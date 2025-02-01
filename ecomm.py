from flask import Flask, render_template_string, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


products = [
    {
        "id": 1,
        "name": "Product 1",
        "description": "Description for Product 1",
        "price": 19.99,
        "image": "https://via.placeholder.com/150"
    },
    {
        "id": 2,
        "name": "Product 2",
        "description": "Description for Product 2",
        "price": 29.99,
        "image": "https://via.placeholder.com/150"
    }
]

base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <title>E-Commerce Website</title>
</head>
<body>
    <header>
        <h1>Local Business E-Commerce</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('cart') }}">Cart ({{ session.get('cart', []).count }})</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2023 Local Business</p>
    </footer>
</body>
</html>
"""


index_template = """
{% extends 'base.html' %}

{% block content %}
<h2>Products</h2>
<div class="product-list">
    {% for product in products %}
    <div class="product">
        <img src="{{ product.image }}" alt="{{ product.name }}">
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}</p>
        <p>${{ product.price }}</p>
        <a href="{{ url_for('product', product_id=product.id) }}">View Details</a>
        <a href="{{ url_for('add_to_cart', product_id=product.id) }}">Add to Cart</a>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""


product_template = """
{% extends 'base.html' %}

{% block content %}
<h2>{{ product.name }}</h2>
<img src="{{ product.image }}" alt="{{ product.name }}">
<p>{{ product.description }}</p>
<p>${{ product.price }}</p>
<a href="{{ url_for('add_to_cart', product_id=product.id) }}">Add to Cart</a>
<a href="{{ url_for('index') }}">Back to Products</a>
{% endblock %}
"""


cart_template = """
{% extends 'base.html' %}

{% block content %}
<h2>Your Cart</h2>
<ul>
    {% for product_id in cart %}
    {% set product = products[product_id - 1] %}
    <li>{{ product.name }} - ${{ product.price }}</li>
    {% endfor %}
</ul>
<a href="{{ url_for('index') }}">Continue Shopping</a>
{% endblock %}
"""

@app.route('/')
def index():
    return render_template_string(index_template, products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template_string(product_template, product=product)

@app.route('/cart')
def cart():
    return render_template_string(cart_template, cart=session.get('cart', []), products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)