from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User, Thuoc, BenhNhan, KhamBenh, Benh, PhieuKhamBenh
import utils
from sqlalchemy import cast, Date

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


@app.route("/api/tim-benh-nhan", methods=['get'])
def tim_benh_nhan():
    kw = request.args.get("kw")
    type = request.args.get("type")
    danhSach = []
    if(type == "tim_kiem_theo_ngay"):
        danhSach = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan==BenhNhan.id).filter(cast(KhamBenh.ngayKham, Date)==kw)
    elif(type == "tim_kiem_theo_ten"):
        danhSach = BenhNhan.query.filter(BenhNhan.ten.like("%" + kw + "%"))
    else:
        danhSach = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan == BenhNhan.id). \
            join(PhieuKhamBenh, KhamBenh.id == PhieuKhamBenh.id_KhamBenh).join(Benh, Benh.id == PhieuKhamBenh.id_Benh).filter(
            Benh.ten.like("%" + kw + "%"))
    res = []
    for i in danhSach:
        res.append({"id": i.id, "ten":i.ten, "gioi_tinh": i.gioiTinh, "dia_chi": i.diaChi, "ngay_sinh":i.ngaySinh, "SDT":i.soDT})
    return jsonify({"danh_sach": res})

@app.route("/api/lich-su-kham-benh", methods=['get'])
def lich_su_kham_benh():
    id = request.args.get("id")
    benh_nhan = BenhNhan.query.get(int(id))
    res = []
    for i in benh_nhan.cacLanKham:
        don_thuoc = []
        for item in i.phieuKham.don_thuoc:
            don_thuoc.append({"ten": item.thuoc.tenThuoc, "so_luong": item.soLuong, "cach_dung": item.cachDung.ten})
        res.append({"id": i.id, "ngay_kham": i.ngayKham, "trieu_chung": i.phieuKham.trieuChung,
                    "benh": i.phieuKham.benh.ten, "bac_si": i.phieuKham.bacSi.thongTin.ten,
                    "don_thuoc": don_thuoc})

    return jsonify({"danh_sach": res})