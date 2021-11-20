from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import *
import utils
from sqlalchemy import insert
from datetime import date
from sqlalchemy import cast, Date


@app.route('/nurse')
def nurse_home():
    return render_template("nurse_home.html")

@app.route('/add-victim', methods=["get"])
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

@app.route('/them-dskham')
def them_dskham():
    id = request.args.get("id")
    today = date.today()

    metadata = db.MetaData()
    kham_benh = db.Table('kham_benh', metadata, autoload=True, autoload_with=db.engine)

    stmt = (
        insert(kham_benh).
            values(id_BenhNhan = id, ngayKham = today)
    )
    connection = db.engine.connect()
    connection.execute(stmt)
    return redirect("/nurse")


@app.route('/api/xem-dskham/<date>', methods=["get"])
def ds_kham(date):
    danhSach = BenhNhan.query.join(KhamBenh, BenhNhan.id==KhamBenh.id_BenhNhan).filter(cast(KhamBenh.ngayKham, Date)==date) \
        .add_columns(BenhNhan.ten, BenhNhan.soDT, KhamBenh.ngayKham)

    print(danhSach)
    res = []
    for i in danhSach:
        res.append({"ten": i.ten, "SDT": i.soDT, "ngay_kham": i.ngayKham})
    return jsonify({"danh_sach": res})

