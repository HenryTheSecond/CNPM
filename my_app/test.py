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

a = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan==BenhNhan.id).\
    join(PhieuKhamBenh, KhamBenh.id==PhieuKhamBenh.id_KhamBenh).join(Benh, Benh.id==PhieuKhamBenh.id_Benh).filter(Benh.ten.like("%" + "sốt" + "%"))

a = BenhNhan.query.join(KhamBenh, KhamBenh.id_BenhNhan==BenhNhan.id).filter(cast(KhamBenh.ngayKham, Date)==datetime(year=2021, month=10, day=23))

for item in a:
    print(item.ten)



