from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import *
import utils
from sqlalchemy import insert
from datetime import date
from sqlalchemy import cast, Date


@app.route('/nurse')
def nurse_home():
    return render_template("nurse/nurse_home.html")

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

    res = []
    for i in danhSach:
        res.append({"ten": i.ten, "SDT": i.soDT, "ngay_kham": i.ngayKham})
    return jsonify({"danh_sach": res})

@app.route('/api/ds-duyet-lich', methods=['get'])
def ds_duyet_lich():
    danhSach = DangKyOnline.query.join(TamThoiLuuTru, DangKyOnline.id==TamThoiLuuTru.id)\
            .filter(TamThoiLuuTru.trangThai==1)\
            .join(BenhNhan, DangKyOnline.id_BenhNhan==BenhNhan.id)\
            .add_columns(BenhNhan.id, BenhNhan.ten, DangKyOnline.ngayKhamDangKy, DangKyOnline.soDT, DangKyOnline.id.label('id_dk'))

    res = []
    for i in danhSach:
        res.append({"id": i.id, "ten": i.ten, "ngay_dk_kham": i.ngayKhamDangKy, "so_dt": i.soDT, "id_dk": i.id_dk})
    return jsonify({"danh_sach": res})


@app.route('/api/delete-luu-tam-thoi/<id>', methods=['delete'])
def delete_luu_tam_thoi(id):
    luu_tam_thoi = TamThoiLuuTru.query.get(id)
    db.session.delete(luu_tam_thoi)
    db.session.commit()

    return jsonify({
        "error_code": 200,
    })


@app.route('/api/them-ds-kham', methods=['post'])
def them_ds_kham():
    data = request.json

    metadata = db.MetaData()
    kham_benh = db.Table('kham_benh', metadata, autoload=True, autoload_with=db.engine)

    stmt = (
        insert(kham_benh).
            values(id_BenhNhan=data['id_benh_nhan'], ngayKham=data['ngay_kham_dk'])
    )
    connection = db.engine.connect()
    connection.execute(stmt)
    return jsonify({
        "error_code": 200
    })


@app.route('/api/delete-dk-onl/<id>', methods=['delete'])
def delete_dk_onl(id):
    dk_onl = DangKyOnline.query.get(int(id))
    if dk_onl.isKhamLanDau == 1:
        benh_nhan = BenhNhan.query.get(int(dk_onl.id_BenhNhan))
        db.session.delete(benh_nhan)

    db.session.delete(dk_onl)
    db.session.commit()

    return jsonify({
        "error_code": 200,
    })

@app.route("/api/gui_sms", methods=['post'])
def gui_sms():
    data = request.json
    return jsonify(utils.gui_sms(data["SDT"], data["message"]))

