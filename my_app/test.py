from models import *
from datetime import datetime
from sqlalchemy import func, cast, Date
from my_app import db

date = datetime(year=2021, month=10, day=23)

'''a = db.session.query(func.sum(HoaDon.total))\
    .join(PhieuKhamBenh, HoaDon.id_KhamBenh==PhieuKhamBenh.id_KhamBenh)\
    .join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id_BenhNhan)\
    .filter(KhamBenh.ngayKham==date).first()


print(a[0]==None)'''

'''a = BenhNhan.query.join(KhamBenh, BenhNhan.id==KhamBenh.id_BenhNhan).filter(KhamBenh.ngayKham==date).add_columns(KhamBenh.ngayKham)\
    .join(PhieuKhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id)\
    .join(HoaDon, HoaDon.id_KhamBenh==PhieuKhamBenh.id_KhamBenh).add_columns(HoaDon.total)

b= PhieuKhamBenh.query.join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id).filter(KhamBenh.ngayKham==date).add_columns(KhamBenh.ngayKham)\
    .join(BenhNhan, KhamBenh.id_BenhNhan==BenhNhan.id).add_columns(BenhNhan.id, BenhNhan.ten)

temp = []
for i in a:
    temp.append({"ten":i[0].ten, "ngay_kham":i.ngayKham, "total":i.total})
print(temp)'''

'''a = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan==BenhNhan.id).\
    join(PhieuKhamBenh, KhamBenh.id==PhieuKhamBenh.id_KhamBenh).join(Benh, Benh.id==PhieuKhamBenh.id_Benh).filter(Benh.ten.like("%" + "sốt" + "%"))

a = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan==BenhNhan.id).filter(cast(KhamBenh.ngayKham, Date)==datetime(year=2021, month=10, day=23))

for item in a:
    print(item.ten)'''

#a = BenhNhan.query.get(1)

#print(a.cacLanKham)

'''res = []
for i in a.cacLanKham:
    don_thuoc = []
    for item in i.phieuKham.don_thuoc:
        don_thuoc.append({"ten": item.thuoc.tenThuoc, "so_luong": item.soLuong, "cach_dung": item.cachDung.ten})
    res.append({"id": i.id, "ngay_kham":i.ngayKham, "trieu_chung": i.phieuKham.trieuChung,
                "benh": i.phieuKham.benh.ten, "bac_si":i.phieuKham.bacSi.thongTin.ten,
                "don_thuoc": don_thuoc})

for i in res:
    print(i)

print(Benh.query.all())'''

#a = KhamBenh.query.filter(KhamBenh.id_BenhNhan == 1).filter(cast(KhamBenh.ngayKham, Date) == datetime.now().date()).first()
#print(a.ngayKham)


'''danhSach = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan == BenhNhan.id).filter(BenhNhan.ten.like("%" + "tuy" + "%")).\
            filter(cast(KhamBenh.ngayKham, Date)==datetime.now().date()).add_columns(KhamBenh.id).all()




for i in danhSach:
    print(i.ten)'''


'''benh_nhan = BenhNhan.query.get(int('1'))
res = []
for i in benh_nhan.cacLanKham:
        don_thuoc = []
        for item in i.phieuKham.don_thuoc:
            don_thuoc.append({"ten": item.thuoc.tenThuoc, "so_luong": item.soLuong, "cach_dung": item.cachDung.ten})
        res.append({"id": i.id, "ngay_kham": i.ngayKham, "trieu_chung": i.phieuKham.trieuChung,
                    "benh": i.phieuKham.benh.ten, "bac_si": i.phieuKham.bacSi.thongTin.ten,
                    "don_thuoc": don_thuoc})


print(res)'''

a = TienKham.query.first()
print(a.gia)