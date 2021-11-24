from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
app.config["SQLALCHEMY_DATABASE_URI"] =f"mysql+pymysql://{db_username}:{db_password}@localhost/cnpm?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key="123456789"
#app.config["PAGE_SIZE"]=6

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Phòng mạch", template_mode="bootstrap4")
my_login = LoginManager(app=app)

#CART_KEY = "cart"
