from app import app, db
from flask import render_template, request, redirect, session, flash, url_for, jsonify, send_from_directory,Flask, send_file, jsonify
from app.models import User, Product, ImageData, Category,Transaction
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import io


UPLOAD_FOLDER = 'app/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#Admin Management

@app.route("/admin_login", methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        load_dotenv()
        admin_user_name = os.environ.get("ADMIN_LOGIN")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if email == admin_user_name and password == admin_password:
            session["email"] = admin_user_name
            flash("Logged in to Admin Dashboard")
            return redirect('/admin_dashboard')
        else:
            flash("Incorrect Password or Email, Try Again")
            return render_template('admin_login.html')
    
    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    
    if "email" in session and session["email"] == admin_user_name:
        # Query all users
        users = User.query.all()
        
        # Calculate total sales
        total_sales = db.session.query(db.func.sum(Transaction.total_amount)).scalar() or 0

        # Count total users
        total_users = User.query.count()

        # Count total products
        total_products = Product.query.count()  # Count total products

        # Prepare data for the pie chart (e.g., sales by status)
        sales_by_status = db.session.query(
            Transaction.status,
            db.func.sum(Transaction.total_amount)
        ).group_by(Transaction.status).all()

        # Convert data for the pie chart
        pie_labels = [status for status, _ in sales_by_status]
        pie_data = [amount for _, amount in sales_by_status]

        return render_template(
            "admin_dashboard.html",
            users=users,
            total_sales=total_sales,
            total_users=total_users,
            total_products=total_products,  # Pass total products to template
            pie_labels=pie_labels,
            pie_data=pie_data
        )  # Pass all necessary data to the template

    return redirect('/admin_login')

#User Blocking and unblocking Management

@app.route('/admin_dashboard/block_user/<int:id>', methods=['POST'])
def block_user(id):
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if session["email"] == admin_user_name:
        
        user = User.query.get(id)
        if user:
            user.is_blocked = True
            db.session.commit()
            flash(f"User {user.email} has been blocked.", "success")
    return redirect(url_for('admin_dashboard'))

# ensure that you check that only admin is allowed to access this route 
@app.route('/admin_dashboard/unblock_user/<int:id>', methods=['POST'])
def unblock_user(id):
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if session["email"] == admin_user_name:
        
        user = User.query.get(id)
        if user:
            user.is_blocked = False
            db.session.commit()
            flash(f"User {user.email} has been unblocked.", "success")
    return redirect(url_for('admin_dashboard'))


## CATEGORY MANAGEMENT ##
@app.route('/add_category')
def add_category():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
    
        categories = Category.query.all()
        return render_template('add_category.html', categories=categories)
    return redirect('/admin_login')

@app.route('/api/add_category', methods=['POST'])
def api_add_category():
    data = request.get_json()
    category_name = data.get("categoryName")

    if not category_name:
        return jsonify({"success": False, "error": "No category name provided"}), 400

    new_category = Category(name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"success": True, "category_id": new_category.id})

@app.route('/api/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"success": False, "error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"success": True})

## PRODUCT MANAGEMENT ##
@app.route("/add_product", methods=['GET', 'POST'])
def add_product():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:    
        categories = Category.query.all()

        if request.method == 'POST':
            product_name = request.form['productName']
            product_price = request.form['productPrice']
            available_qty = request.form['availableQuantity']
            description = request.form['description']
            category_id = request.form['productCategory']

            image_file = request.files.get('productImage')
            image_id = None  # Default if no image is uploaded

            if image_file:
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)

                new_image = ImageData(filename=filename)
                db.session.add(new_image)
                db.session.commit()

                image_id = new_image.id  # Store the image ID in the product table
            print(image_id)
            print(product_name)
            print(available_qty)

            new_product = Product(
                product_name=product_name,
                price=product_price,
                av_qty=available_qty,
                description=description,
                category_id=category_id,
                image_id=image_id  # Store image reference
            )

            db.session.add(new_product)
            db.session.commit()
            flash("Product Added Successfully!", 'success')
            return redirect('/admin_dashboard')

        return render_template('add_product.html', categories=categories)
    return redirect('/admin_login')

##Editing Products Management
@app.route('/edit_product')
def edit_pro():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
        products = Product.query.all()

        product_data = []
        for product in products:
            image = ImageData.query.get(product.image_id) if product.image_id else None
            
            image_url = image.get_image_url() if image else url_for('static', filename='default.jpg')

            product_data.append({
                "name": product.product_name,
                "price": product.price,
                "description": product.description,
                "quantity": product.av_qty,
                "image_path": image_url,
                "product_id": product.id  # Include product ID for editing functionality
            })

        return render_template("edit_pro.html", products=product_data)
    return redirect('/admin_login')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
        product = Product.query.get(product_id)
        if not product:
            return redirect('/edit_product')

        if request.method == 'POST':
            # Update product details
            product.product_name = request.form.get('name')
            product.price = request.form.get('price')
            product.description = request.form.get('description')
            product.av_qty = request.form.get('quantity')
            
            # Handle image upload
            image_file = request.files.get('image')
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)

                # Remove old image if exists
                if product.image_id:
                    old_image = ImageData.query.get(product.image_id)
                    if old_image:
                        db.session.delete(old_image)

                # Save new image data
                new_image = ImageData(filename=filename)
                db.session.add(new_image)
                db.session.commit()
                product.image_id = new_image.id
            
            db.session.commit()
            print(f"Product with ID {product_id} has been updated.")
            return redirect('/edit_product')  # Redirect after editing

        return render_template("edit_product_form.html", product=product)  # Render form with product data
    return redirect('/admin_login')


## Deleting Product Management
@app.route('/delete_product')
def delete_pro():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
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
                "image_path": image_url,
                "product_id": product.id  # Include product ID for the delete functionality
            })
        return render_template("delete_pro.html", products=product_data)
    return redirect('/admin_login')

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
        product = Product.query.get(product_id)
        if product:
            # Delete the associated image if it exists (optional)
            if product.image_id:
                image = ImageData.query.get(product.image_id)
                if image:
                    # Delete the image file from the filesystem (if required)
                    # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                    db.session.delete(image)            
            db.session.delete(product)
            db.session.commit()
            print(f"Product with ID {product_id} has been deleted.")
            return redirect('/delete_product')
    return redirect('/admin_login')


#Transaction Management
@app.route('/admin/transactions')
def admin_transactions():
    admin_user_name = os.environ.get("ADMIN_LOGIN")
    if "email" in session and session["email"] == admin_user_name:
        try:
            transactions = Transaction.query.all()   
            if not transactions:
                flash("No transactions found!", "warning")  # Optional: Flash message
            print(transactions)    
            return render_template('admin_transactions.html', transactions=transactions)
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return "An error occurred while fetching transactions", 500
    return redirect('/admin_login')

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    flash("Admin has been Logged Out!", 'error')
    return redirect("/admin_login")