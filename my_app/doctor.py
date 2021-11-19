from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User, Thuoc
import utils

@app.route('/doctor')
def doctor_home():
    return render_template("doctor/doctor_home.html")

@app.route("/api/tim-thuoc", methods=['get'])
def tim_thuoc():
    kw = request.args.get("kw")
    print(kw)
    danhSach = Thuoc.query.filter(Thuoc.tenThuoc.like("%" + kw + "%")).all()
    res = []
    for i in danhSach:
        res.append({"id": i.id, "ten_thuoc": i.tenThuoc, "don_vi": i.donVi.ten, "gia": i.gia, "so_luong":i.soLuong})
    return jsonify({"danh_sach": res})


