from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify
from flask_session import Session
from markupsafe import escape
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Define the directory to save files
UPLOAD_FOLDER = "./app/static/product_image"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Base(DeclarativeBase):
    pass

app = Flask(__name__, static_folder='static')

# ✅ Use Postgres from Render environment
database_url = os.environ.get("DATABASE_URL")

# Fix old postgres:// to postgresql://
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize database
db = SQLAlchemy(app, model_class=Base)

# Session config
app.secret_key = 'satyam_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ✅ ✅ Automatically create tables on startup (free alternative to Shell)
with app.app_context():
    db.create_all()

# ✅ Import your routes after app + db are defined
from app.routes_users import *
from app.routes_admin import *
from app.models import *
