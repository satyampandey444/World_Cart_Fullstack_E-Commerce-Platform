from app import app,db,os
from app.routes_users import *
from app.routes_admin import *
from app.models import Product,ImageData,Category,Transaction
from app.helping_functions import read_image_as_binary
from sqlalchemy.exc import OperationalError
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Function to safely query the database with retry logic
def safe_db_query(query_func, max_retries=5, delay=0.5):
    retries = 0
    while retries < max_retries:
        try:
            # Run the query
            return query_func()
        except OperationalError:
            # If database is locked, wait for a while and retry
            time.sleep(delay)
            retries += 1
            print(f"Database is locked. Retrying ({retries}/{max_retries})...")
    # If max retries are exhausted, raise an exception
    raise Exception("Database is locked and could not be accessed after multiple retries.")

# Query to get users and products
def get_users():
    return db.session.execute(db.select(User).order_by(User.email)).scalars()

def get_products():
    return db.session.execute(db.select(Product).order_by(Product.product_name)).scalars()


if __name__=='__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()

        try:
            # Fetch users and products with retry logic
            users = safe_db_query(get_users)
            products = safe_db_query(get_products)

            print("Users:", list(users))
            print("Products:", list(products))

        except Exception as e:
            print(f"Error: {e}")
        app.run(debug=True) 
        