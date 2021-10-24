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

    danhSach = BenhNhan.query.join(KhamBenh, BenhNhan.id==KhamBenh.id_BenhNhan).filter(KhamBenh.ngayKham==date)\
        .add_columns(KhamBenh.ngayKham, BenhNhan.ten)\
    .join(PhieuKhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id)\
    .join(HoaDon, HoaDon.id_KhamBenh==PhieuKhamBenh.id_KhamBenh).add_columns(HoaDon.total)
    res = []
    for i in danhSach:
        res.append({"ten": i[0].ten, "ngay_kham": i.ngayKham, "total": i.total})
    return jsonify({"danh_sach": res})

if __name__ == '__main__':
    app.run(debug=True)