from flask import Flask,render_template,redirect,request,session,flash, url_for
from flask_session import Session
from markupsafe import escape
from sqlalchemy import Integer, String ,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import bcrypt
import os
from dotenv import load_dotenv
from flask import jsonify



# Define the directory to save files
UPLOAD_FOLDER = "./app/static/product_image"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class Base(DeclarativeBase):
  pass


app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db?check_same_thread=False"
# initialize the app with the extension
db = SQLAlchemy(app,model_class=Base)
app.secret_key = 'satyam_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

