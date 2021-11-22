from flask import render_template, request, redirect, session, jsonify
from my_app import app, my_login, db
from my_app.models import User, Thuoc, BenhNhan, KhamBenh, Benh, PhieuKhamBenh, CachDung, DonThuoc
import utils
from sqlalchemy import cast, Date
from datetime import datetime
from flask_login import current_user


@app.route('/doctor')
def doctor_home():
    benh = Benh.query.all()
    thuoc = Thuoc.query.all()
    cach_dung = CachDung.query.all()
    return render_template("doctor/doctor_home.html", benh=benh, thuoc=thuoc, cach_dung=cach_dung)

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
        if(i.phieuKham != None):
            don_thuoc = []
            for item in i.phieuKham.don_thuoc:
                don_thuoc.append({"ten": item.thuoc.tenThuoc, "so_luong": item.soLuong, "cach_dung": item.cachDung.ten})
            res.append({"id": i.id, "ngay_kham": i.ngayKham, "trieu_chung": i.phieuKham.trieuChung,
                        "benh": i.phieuKham.benh.ten, "bac_si": i.phieuKham.bacSi.thongTin.ten,
                        "don_thuoc": don_thuoc})

    return jsonify({"danh_sach": res})


@app.route("/lap-phieu", methods = ['post'])
def lap_phieu_kham_benh():
    chi_tiet = request.form.getlist("don_thuoc_chi_tiet")
    cach_dung = request.form.getlist("cach_dung")
    so_luong = request.form.getlist("so_luong")
    id_kham_benh = request.form.get("id")
    trieu_chung = request.form.get("trieu_chung")
    benh = request.form.get("benh")
    phieu_kham_benh = PhieuKhamBenh(id_KhamBenh=id_kham_benh, trieuChung=trieu_chung, id_Benh=int(benh), id_BacSi= current_user.id )
    db.session.add(phieu_kham_benh)
    for i in range(0, len(chi_tiet)):
        if(so_luong[i] !='0' and so_luong[i]!=''):
            don_thuoc = DonThuoc(id_KhamBenh=id_kham_benh, id_Thuoc=chi_tiet[i], soLuong=so_luong[i], id_CachDung=cach_dung[i])
            db.session.add(don_thuoc)
    db.session.commit()
    return redirect("/doctor")


@app.route("/api/tim-benh-nhan-kham-benh", methods=['get'])
def tim_benh_nhan_kham_benh():
    kw = request.args.get("kw")
    danhSach = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan == BenhNhan.id).filter(
        BenhNhan.ten.like("%" + kw + "%")). \
        filter(cast(KhamBenh.ngayKham, Date) == datetime.now().date()).add_columns(KhamBenh.id).all()
    res = []
    for i in danhSach:
        res.append({"id": i[0].id, "id_kham_benh":i[1], "ten": i[0].ten, "gioi_tinh": i[0].gioiTinh, "dia_chi": i[0].diaChi, "ngay_sinh": i[0].ngaySinh,
                    "SDT": i[0].soDT})
    return jsonify({"danh_sach": res})


