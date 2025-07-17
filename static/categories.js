function loadContent(category) {
  let endpoint = '';
  if (category === 'veg') {
    endpoint = 'veg-content';
  } else if (category === 'nonveg') {
    endpoint = 'non-veg-content';
  } else {
    console.error('Invalid category selected.');
    return;
  }

  fetch(`/${endpoint}`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      return res.text();
    })
    .then(data => {
      const container = document.getElementById('category-content');
      container.innerHTML = data;
      container.scrollIntoView({ behavior: 'smooth' });

      // Ensure addToCart works for newly injected content
      window.addToCart = addToCart;
    })
    .catch(err => {
      document.getElementById('category-content').innerHTML =
        "<p class='text-center text-danger'>Unable to load content. Please try again.</p>";
      console.error("Fetch error:", err);
    });
}

function addToCart(name, price, image) {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  const existing = cart.find(item => item.name === name);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ name, price, image, quantity: 1 });
  }
  localStorage.setItem('cart', JSON.stringify(cart));
  alert(`${name} added to cart!`);

  // Sync with Flask backend
  fetch('/add-to-cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `item_name=${encodeURIComponent(name)}&price=${price}`
  })
  .then(response => {
    if (!response.ok) {
      console.error("Failed to sync cart with backend.");
    }
  })
  .catch(error => {
    console.error("Error syncing with backend:", error);
  });
}
