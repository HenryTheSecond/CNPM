from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User
import utils

@app.route('/nurse')
def nurse_home():
    return render_template("nurse_home.html")
