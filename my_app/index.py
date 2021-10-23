from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login
from my_app.models import User
from admin import *
import hashlib
from flask_login import login_user
from sqlalchemy import func
import utils

@app.route("/")
def home():
    return render_template("home.html")


@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=['post'])
def login_exe():
    username = request.form.get("username")
    password = request.form.get("password")

    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    if user:
        login_user(user)

    return redirect("/admin")


@app.route("/api/doanh-thu-ngay/<date>", methods=['get'])
def doanh_thu_ngay(date):
    doanhthu = db.session.query(func.sum(HoaDon.total))\
    .join(PhieuKhamBenh, HoaDon.id_KhamBenh==PhieuKhamBenh.id_KhamBenh)\
    .join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id_BenhNhan)\
    .filter(KhamBenh.ngayKham==date).first()

    return jsonify({
        "doanh_thu_ngay": doanhthu[0]
    })

if __name__ == '__main__':
    app.run(debug=True)