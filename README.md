![GitHub stars](https://img.shields.io/github/stars/Karthi-Natarajan/Zomato-Style-Food-web-page?style=social)
![GitHub forks](https://img.shields.io/github/forks/Karthi-Natarajan/Zomato-Style-Food-web-page?style=social)
![GitHub license](https://img.shields.io/github/license/Karthi-Natarajan/Zomato-Style-Food-web-page)

# 🍽️ InstaFood – Zomato-Style Food Ordering Website

A full-stack web application inspired by Zomato, where users can browse food items (Veg, Non-Veg, Both), add them to cart, and place orders. The project features user authentication (Signup/Login), category-wise item display, cart functionality using localStorage, and order management via MySQL.

---

## 📌 Features

- 🔐 User Signup & Login (Flask backend with MySQL)
- 🥗 Veg / 🍗 Non-Veg / 🍽️ Both Category selection
- 🛒 Add to Cart using localStorage (JavaScript)
- 📥 Order Placement with total amount stored in MySQL
- 📋 View 'My Orders' page with:
  - User ID
  - User Name
  - Total Amount
- 🎨 Responsive, clean UI using HTML, CSS, JS

---

## 🛠️ Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Frontend    | HTML, CSS, JavaScript |
| Backend     | Python (Flask)     |
| Database    | MySQL              |

---

## 🗂️ Project Structure

InstaFood/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── categories.html
│   ├── cart.html
│   └── myorders.html
│
├── app.py
├── requirements.txt
└── README.md


## How to Run the project
# 1. Clone the repo
git clone https://github.com/your-username/InstaFood.git
cd InstaFood

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py


## 💾 Database Setup
# Open MySQL and run the following:

CREATE DATABASE instafood;

USE instafood;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    pass VARCHAR(100),
    amount FLOAT
);

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    price FLOAT
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_amount FLOAT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);


## Add your database credentials to app.py:


mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="instafood"
)


## 📃 License
# This project is open-source. Feel free to use and modify it!

