from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User
import utils
from sqlalchemy import insert



@app.route('/nurse')
def nurse_home():
    return render_template("nurse_home.html")

@app.route('/add-victim', methods=["post"])
def add_victim():
    name = request.form.get("name")
    gender = request.form.get("gender")
    address = request.form.get("address")
    birthdate = request.form.get("birthdate")
    phone = request.form.get("phone")

    metadata = db.MetaData()
    benh_nhan = db.Table('benh_nhan', metadata, autoload=True, autoload_with=db.engine)

    stmt = (
        insert(benh_nhan).
            values(ten = name, gioiTinh = gender, diaChi = address, ngaySinh = birthdate, soDT = phone)
    )
    connection = db.engine.connect()
    connection.execute(stmt)
    return redirect("/nurse")

