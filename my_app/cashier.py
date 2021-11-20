from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import *
import utils
from sqlalchemy import insert
from datetime import date
from sqlalchemy import literal, Unicode


@app.route('/cashier')
def cashier_home():
    return render_template("cashier/cashier_home.html")

@app.route('/api/xem-ds-phieu', methods=["get"])
def ds_phieu():
    danhSach = PhieuKhamBenh.query.join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id) \
        .join(BenhNhan, KhamBenh.id_BenhNhan==BenhNhan.id)\
        .join(Benh, PhieuKhamBenh.id_Benh==Benh.id)\
        .add_columns(KhamBenh.id, BenhNhan.ten, PhieuKhamBenh.trieuChung, Benh.ten, literal("Benh.ten", type_=Unicode).label('benh_ten'))

    print(danhSach)
    res = []
    for i in danhSach:
        res.append({"kham_benh_id": i.trieuChung, "sdfds": i.benh_ten})
    return jsonify({"danh_sach": res})

