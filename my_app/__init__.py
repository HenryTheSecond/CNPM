from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
#from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:congtuyen2032001@localhost/cnpm?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key="123456789"
app.config["PAGE_SIZE"]=6

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Phong mach", template_mode="bootstrap4")
#my_login = LoginManager(app=app)

CART_KEY = "cart"
