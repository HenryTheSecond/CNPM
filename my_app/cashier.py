from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import *
import utils
from sqlalchemy import insert
from datetime import date


@app.route('/cashier')
def cashier_home():
    return render_template("cashier/cashier_home.html")

@app.route('/api/xem-ds-phieu', methods=["get"])
def ds_phieu():
    danhSach = PhieuKhamBenh.query.join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id) \
        .join(BenhNhan, KhamBenh.id_BenhNhan==BenhNhan.id)\
        .join(Benh, PhieuKhamBenh.id_Benh==Benh.id)\
        .add_columns(KhamBenh.id, BenhNhan.ten, PhieuKhamBenh.trieuChung, KhamBenh.ngayKham, Benh.ten.label('ten_benh'))

    print(danhSach)
    res = []
    for i in danhSach:
        res.append({"kham_benh_id": i.id, "ten_benh_nhan": i.ten, "trieu_chung": i.trieuChung, "ngay_kham": i.ngayKham, "ten_benh": i.ten_benh})
    return jsonify({"danh_sach": res})

