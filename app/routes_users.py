from app import app, db
from flask import render_template, request, redirect, session, flash, url_for, jsonify, send_from_directory,Flask, send_file, jsonify
from app.models import User, Product, ImageData, Category,Transaction
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import io
from datetime import datetime
import json

UPLOAD_FOLDER = 'app/static/product_image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/login', methods=['POST', 'GET'])
def api():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            if user.is_blocked:
                flash("You are blocked. Contact Admin.", 'error')
                return redirect('/login')
            
            if user.check_password(password):
                session["user_id"] = user.id  # ✅ Store user ID in session
                session["email"] = email
                flash(f"{email} logged in successfully!", 'success')
                return redirect('/dashboard')
            else:
                flash("Invalid password. Try again!", 'error')
        else:
            flash("User not found. Please sign up!", 'error')
            return redirect('/signup')

    flash("Login Failed!", 'error')   
    return render_template('login.html')

@app.route('/api/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists! Please use a different email.")
        return redirect('/register')

    new_user = User(first=first_name, last=last_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash("You are now Signed Up")
    return redirect('/login')

@app.route('/dashboard')
def index():
    if "email" in session:
        products = Product.query.all()

        product_data = []
        for product in products:
            image = ImageData.query.get(product.image_id) if product.image_id else None
            
            
            if image:
                image_url = image.get_image_url()
                print(image_url)
            else:
                image_url = url_for('static', filename='default.jpg')
                print('image not found')

            product_data.append({
                "name": product.product_name,
                "price": product.price,
                "description": product.description,
                "quantity": product.av_qty,
                "image_path": image_url
            })

        return render_template("dashboard.html", products=product_data)
    return redirect('/signup')

@app.route('/static/product_image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Other imports and configurations...
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    orders = Transaction.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        if 'edit_profile' in request.form:
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            if new_email:
                user.email = new_email
            if new_password:
                user.set_password(new_password)  # Hash the new password
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        elif 'delete_account' in request.form:
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
            flash('Account deleted successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('profile.html', user=user, orders=orders)

# Ensure you have a method to hash passwords in your User model

#fetching the product to display on the dashboard
@app.route('/categories_display')
def categories_display():
    categories = Category.query.all()
    return render_template('categories_display.html', categories=categories)

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    
    total_price = sum(item["price"] * item["quantity"] for item in cart.values())

    return render_template("cart.html", cart=cart, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get("id")
    name = request.form.get("name")
    price = request.form.get("price")

    if not product_id or not name or not price:
        return "Invalid data", 400

    try:
        price = float(price)
    except ValueError:
        return "Invalid price format", 400

    cart = session.get("cart", {})

    if product_id in cart:
        cart[product_id]["quantity"] += 1
    else:
        cart[product_id] = {"name": name, "price": price, "quantity": 1}

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get("id")
    action = request.form.get("action")

    cart = session.get("cart", {})

    if product_id in cart:
        if action == "increase":
            cart[product_id]["quantity"] += 1
        elif action == "decrease":
            cart[product_id]["quantity"] -= 1
            if cart[product_id]["quantity"] <= 0:
                del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get("id")
    
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    
    session["cart"] = cart
    session.modified = True
    
    return redirect(url_for("cart"))




@app.route("/logout")
def logout():
    session.clear()
    flash("You have been Logged Out!", 'error')
    return redirect("/login")



@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('cart'))

    cart_items = session.get('cart', {})

    # Ensure cart is a dictionary
    if not isinstance(cart_items, dict):
        flash("Invalid cart data!", "danger")
        return redirect(url_for('cart'))

    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_items.values())

    # Ensure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to checkout!", "danger")
        return redirect(url_for('login'))

    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        items=cart_items,  # Store cart as JSON
        total_amount=total_price,
        status="Done",
        date=datetime.now()
    )

    # Deduct stock
    for product_name, item in cart_items.items():
        product = Product.query.filter_by(product_name=product_name).first()  # Fetch product by correct field
        if product:
            if product.av_qty >= item['quantity']:
                product.av_qty -= item['quantity']  # Deduct from available quantity
            else:
                flash(f"Not enough stock for {product_name}", "danger")
                return redirect(url_for('cart'))
        else:
            flash(f"Product '{product_name}' not found!", "danger")
            return redirect(url_for('cart'))

    
    db.session.add(transaction)
    db.session.commit()

    session.pop('cart', None)  # Clear cart

    flash("Order placed successfully!", "success")
    return render_template('checkout.html', total_price=total_price)


@app.route('/search_page')
def search_page():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return render_template('search.html', results=[])

    filtered_products = Product.query.filter(
        (Product.product_name.ilike(f"%{query}%")) | 
        (Product.description.ilike(f"%{query}%"))
    ).all()

    results = []
    for product in filtered_products:
        image = ImageData.query.get(product.image_id) if product.image_id else None
        image_url = image.get_image_url() if image else url_for('static', filename='default.jpg')

        results.append({
            "id": product.id,
            "name": product.product_name,
            "price": product.price,
            "description": product.description,
            "image_path": image_url
        })

    return render_template('search.html', results=results)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/new_products")
def new_products():
    if "email" in session:
        products = Product.query.all()

        product_data = []
        for product in products:
            image = ImageData.query.get(product.image_id) if product.image_id else None
            
            
            if image:
                image_url = image.get_image_url()
                print(image_url)
            else:
                image_url = url_for('static', filename='default.jpg')
                print('image not found')

            product_data.append({
                "name": product.product_name,
                "price": product.price,
                "description": product.description,
                "quantity": product.av_qty,
                "image_path": image_url
            })

        return render_template("new_products.html",products=product_data)
    return redirect('/signup')