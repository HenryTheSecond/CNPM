from flask import render_template, request, redirect, session, jsonify
from my_app import app
#from my_app.models import User
from admin import *
import hashlib
#from flask_login import login_user
import utils

@app.route("/")
def home():
    return render_template("home.html")






if __name__ == '__main__':
    app.run(debug=True)