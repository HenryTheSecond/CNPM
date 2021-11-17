from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User
from admin import *
import hashlib
from flask_login import login_user
from sqlalchemy import func
import utils
from nurse import *




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

@app.route("/user-login", methods=['get', 'post'])
def normal_user_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user:
            login_user(user)

        if user.role_Id == 2:
            return redirect("/doctor")
        elif user.role_Id == 3:
            return redirect("/nurse")
    else:
        return render_template("login_user.html")


@app.route("/user-logout")
def normal_user_logout():
    logout_user()
    return redirect("/user-login")

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

@app.route("/api/doanh-thu-thang/<int:month>-<int:year>", methods=['get'])
def doanh_thu_thang(month, year):
    metadata = db.MetaData()
    kham_benh = db.Table('kham_benh', metadata, autoload=True, autoload_with=db.engine)
    hoa_don = db.Table('hoa_don', metadata, autoload=True, autoload_with=db.engine)
    queryDoanhThuThang = db.select([kham_benh.columns.ngayKham, db.func.sum(hoa_don.columns.total).label('doanh_thu_ngay')])\
        .select_from(kham_benh.join(hoa_don, kham_benh.columns.id == hoa_don.columns.id_KhamBenh))\
        .where(db.and_(db.func.month(kham_benh.columns.ngayKham) == month, db.func.year(kham_benh.columns.ngayKham) == year))\
        .group_by(kham_benh.columns.ngayKham)
    print(queryDoanhThuThang)
    connection = db.engine.connect()
    resultProxy = connection.execute(queryDoanhThuThang)
    resultSet = resultProxy.fetchall()
    data = []
    for r in resultSet:
        data.append({"ngay_kham": r[0], "doanh_thu_ngay":r[1]})
    return jsonify({"doanh_thu_ngay": data})


if __name__ == '__main__':
    app.run(debug=True)