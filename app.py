from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ------------------ MySQL Raw Connector Config ------------------
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='anu@21',
        database='zomato_clone'
    )

# ------------------ SQLAlchemy Config ------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:anu%4021@localhost/zomato_clone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ Models ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, default=0)  # Added total_amount column

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# ------------------ Routes ------------------
@app.route('/')
def index():
    name = session.get('user_name')
    return render_template('index.html', name=name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please login.', 'warning')
            return redirect(url_for('login'))

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['user_name'] = name
        session['user_email'] = email
        flash('Signup successful!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    if 'user_name' not in session:
        flash('Please login to access Categories.', 'warning')
        return redirect(url_for('login'))
    return render_template('categories.html', name=session['user_name'])

@app.route('/cart')
def cart():
    if 'user_email' not in session:
        flash('Please login to access Cart.', 'warning')
        return redirect(url_for('login'))

    items = CartItem.query.filter_by(user_email=session['user_email']).all()
    return render_template('cart.html', name=session['user_name'], items=items)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user_email' not in session:
        return "Unauthorized", 401

    item_name = request.form.get('item_name')
    price = request.form.get('price')

    if not item_name or not price:
        return "Missing item name or price", 400

    try:
        price = float(price)
    except ValueError:
        return "Invalid price", 400

    new_item = CartItem(user_email=session['user_email'], item_name=item_name, price=price)
    db.session.add(new_item)
    db.session.commit()

    return "Item added to cart", 200

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        order_data = request.get_json()
        cart = order_data.get('cart')
        address = order_data.get('address')

        if not cart or not address:
            return jsonify({"error": "Cart is empty or address is missing."}), 400

        user_email = session.get('user_email')
        if not user_email:
            return jsonify({"error": "User not logged in."}), 401

        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        user_id = user.id

        total_amount = 0
        order_items = []

        connection = create_connection()
        cursor = connection.cursor()

        for item in cart:
            item_name = item['name']
            quantity = item['quantity']

            cursor.execute("SELECT item_id, price FROM items WHERE item_name = %s", (item_name,))
            result = cursor.fetchone()
            if not result:
                continue

            item_id, price = result
            total_amount += price * quantity
            order_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'price': price
            })

        cursor.close()
        connection.close()

        if not order_items:
            return jsonify({"error": "No valid items found in cart."}), 400

        new_order = Order(user_id=user_id, total_amount=total_amount, delivery_address=address)
        db.session.add(new_order)
        db.session.commit()

        for oi in order_items:
            new_order_item = OrderItem(
                order_id=new_order.id,
                item_id=oi['item_id'],
                quantity=oi['quantity'],
                price=oi['price']
            )
            db.session.add(new_order_item)
        db.session.commit()

        user.total_amount += total_amount
        db.session.commit()

        return jsonify({"message": "Order placed successfully!", "order_id": new_order.id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        orders_data = []
        for order in orders:
            order_items = OrderItem.query.filter_by(order_id=order.id).all()
            items_list = [{
                'item_id': oi.item_id,
                'quantity': oi.quantity,
                'price': oi.price
            } for oi in order_items]

            orders_data.append({
                'order_id': order.id,
                'user_id': order.user_id,
                'total_amount': order.total_amount,
                'delivery_address': order.delivery_address,
                'items': items_list
            })
        return jsonify({"orders": orders_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/veg-content')
def veg_content():
    if 'user_name' not in session:
        return "<p class='text-center'>Please login to view Veg items.</p>"
    return render_template('veg-content.html')

@app.route('/non-veg-content')
def non_veg_content():
    if 'user_name' not in session:
        return "<p class='text-center'>Please login to view Non-Veg items.</p>"
    return render_template('non-veg-content.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)