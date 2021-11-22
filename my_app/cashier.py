from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import *
import utils
from sqlalchemy import insert
from sqlalchemy import update
from datetime import date


@app.route('/cashier')
def cashier_home():
    thuoc = Thuoc.query.all()
    return render_template("cashier/cashier_home.html", thuoc=thuoc)

@app.route('/api/xem-ds-phieu', methods=["get"])
def ds_phieu():
    danhSach = PhieuKhamBenh.query.join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id) \
        .join(BenhNhan, KhamBenh.id_BenhNhan==BenhNhan.id)\
        .join(Benh, PhieuKhamBenh.id_Benh==Benh.id)\
        .filter(PhieuKhamBenh.id_KhamBenh.not_in(db.session.query(HoaDon.id_KhamBenh)))\
        .add_columns(KhamBenh.id, BenhNhan.ten, PhieuKhamBenh.trieuChung, KhamBenh.ngayKham, Benh.ten.label('ten_benh'))

    res = []
    for i in danhSach:
        res.append({"kham_benh_id": i.id, "ten_benh_nhan": i.ten, "trieu_chung": i.trieuChung, "ngay_kham": i.ngayKham, "ten_benh": i.ten_benh})
    return jsonify({"danh_sach": res})

@app.route('/api/create-bill', methods=["post"])
def create_bill():
    data = request.json

    metadata = db.MetaData()
    chi_tiet_hoa_don = db.Table('chi_tiet_hoa_don', metadata, autoload=True, autoload_with=db.engine)

    stmt = (
        insert(chi_tiet_hoa_don).
            values(id_KhamBenh=data["id_kham_benh"], id_Thuoc=data["id_thuoc"], gia=data["gia"], soLuong=data["so_luong"])
    )

    connection = db.engine.connect()
    connection.execute(stmt)
    return jsonify({
        "error_code": 200
    })


@app.route('/api/create-bill-id/<id_kham_benh>', methods=["get"])
def create_bill_id(id_kham_benh):
    stmt = (
        insert(HoaDon).
            values(id_KhamBenh=id_kham_benh)
    )

    connection = db.engine.connect()
    connection.execute(stmt)
    return jsonify({
        "error_code": 200
    })


@app.route('/api/create-bill-total/<id_kham_benh>', methods=["get"])
def create_bill_total(id_kham_benh):
    danhSach = ChiTietHoaDon.query.filter(ChiTietHoaDon.id_KhamBenh == id_kham_benh) \
        .add_columns(ChiTietHoaDon.gia, ChiTietHoaDon.soLuong)

    tong = 0
    for i in danhSach:
        tong += i.gia * i.soLuong
    tong += TienKham.query.first().gia

    stmt = (
        update(HoaDon).
            where(HoaDon.id_KhamBenh == id_kham_benh).
            values(total=tong)
    )
    connection = db.engine.connect()
    connection.execute(stmt)
    return jsonify({
        "error_code": 200
    })




