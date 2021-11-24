from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User
from admin import *
import hashlib
from flask_login import login_user
from sqlalchemy import func
import utils
from nurse import *
from doctor import *
from cashier import *
from flask_cors import CORS
import hmac
import hashlib
import requests


list = []

@app.route("/")
def home():
    return render_template("home.html")


@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

@app.route("/chuyen-trang")
def chuyen_trang():
    role = int(request.args.get("role"));

    if role == 1:
        return redirect("/admin")
    elif role == 2:
        return redirect("/doctor")
    elif role == 3:
        return redirect("/nurse")
    elif role == 4:
        return redirect("/cashier")
    else:
        msg = "Lỗi chuyển trang"

    return render_template('layout/login.html', msg=msg)


@app.route('/dang-ki-online', methods=['get', 'post'])
def dang_ki_online():
    if(request.method == "POST"):
        SDT = request.form.get("SDT")
        ngay_kham = request.form.get("ngay_kham")
        if(request.form.get("da_tung_kham_chua") == 'chua_kham'):
            ten = request.form.get("ten")
            gender = request.form.get("gender")
            dia_chi = request.form.get("dia_chi")
            ngay_sinh = request.form.get("ngay_sinh")
            thoi_gian_dang_ky = datetime.now()
            benh_nhan = BenhNhan(ten=ten, gioiTinh=gender, diaChi=dia_chi, ngaySinh=ngay_sinh, soDT=SDT)
            db.session.add(benh_nhan)
            db.session.commit()
            dang_ky = DangKyOnline(id_BenhNhan=benh_nhan.id, soDT=SDT, ngayDangKy=datetime.now(), ngayKhamDangKy=ngay_kham, isKhamLanDau=True)
            db.session.add(dang_ky)
            db.session.commit()
            tam_thoi_luu_tru = TamThoiLuuTru(id = dang_ky.id, trangThai=True)
            db.session.add(tam_thoi_luu_tru)
        else:
            id_benh_nhan = request.form.get("id")
            dang_ky = DangKyOnline(id_BenhNhan=int(id_benh_nhan), soDT=SDT, ngayDangKy=datetime.now(),
                                   ngayKhamDangKy=ngay_kham, isKhamLanDau=False)
            db.session.add(dang_ky)
            db.session.commit()
            tam_thoi_luu_tru = TamThoiLuuTru(id=dang_ky.id, trangThai=True)
            db.session.add(tam_thoi_luu_tru)
        db.session.commit()
        return render_template('layout/login.html', msg="Đăng kí online thành công")
    return render_template("dk_online/dk_online.html")

@app.route("/login", methods=['post', 'get'])
def login_exe():
    msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user:
            login_user(user)
            if user.role_Id == 1:
                return redirect("/admin")
            elif user.role_Id == 2:
                return redirect("/doctor")
            elif user.role_Id == 3:
                return redirect("/nurse")
            elif user.role_Id == 4:
                return redirect("/cashier")
        else:
            msg = "Sai tài khoản hoặc mật khẩu"

    return render_template('layout/login.html', msg = msg)


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
        elif user.role_Id == 4:
            return redirect("/cashier")
    else:
        return render_template("login_user.html")


@app.route("/user-logout")
def normal_user_logout():
    logout_user()
    return redirect("/login")

@app.route("/api/doanh-thu-ngay/<date>", methods=['get'])
def doanh_thu_ngay(date):
    danhSach = BenhNhan.query.join(KhamBenh, BenhNhan.id==KhamBenh.id_BenhNhan).filter(cast(KhamBenh.ngayKham, Date)==date)\
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


@app.route("/api/thanh-toan-online", methods=['post'])
def thanh_toan_online():
    don_thuoc = request.form.getlist("don_thuoc_select")
    gia_thuoc = request.form.getlist("gia_thuoc_select")
    so_luong = request.form.getlist("so_luong")
    id_kham_benh = request.form.get("id_kham_benh")
    gia = 0
    hoa_don = HoaDon(id_KhamBenh=id_kham_benh, total=TienKham.query.first().gia)
    global list
    list.append(hoa_don)
    db.session.add(hoa_don)
    for i in range(0, len(gia_thuoc)):
        chi_tiet = ChiTietHoaDon(id_KhamBenh= id_kham_benh, id_Thuoc= don_thuoc[i], gia=gia_thuoc[i], soLuong=so_luong[i])
        db.session.add(chi_tiet)
        list.append(chi_tiet)
        gia += int(float(so_luong[i])) * int(float(gia_thuoc[i]))
    hoa_don.total += gia

    r = utils.link_thanh_toan(hoa_don.total)
    return redirect(r.json()['payUrl'])


@app.route("/momo/xu-ly")
def luu_hoa_don():
    global list
    for i in list:
        db.session.add(i)
    db.session.commit()
    list.clear()
    return redirect("/cashier")


if __name__ == '__main__':
    app.run(debug=True)
