from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify
from flask_session import Session
from markupsafe import escape
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "./app/static/product_image"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Base(DeclarativeBase):
    pass

app = Flask(__name__, static_folder='static')

# Load Database URL from Render
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app, model_class=Base)

app.secret_key = 'satyam_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ✅ Import models FIRST
from app.models import *

# ✅ Create tables BEFORE importing routes
with app.app_context():
    db.create_all()

# ✅ Import routes AFTER tables exist
from app.routes_users import *
from app.routes_admin import *
