from models import *
from datetime import datetime
from sqlalchemy import func
from my_app import db

date = datetime(year=2021, month=10, day=23)

a = db.session.query(func.sum(HoaDon.total))\
    .join(PhieuKhamBenh, HoaDon.id_KhamBenh==PhieuKhamBenh.id_KhamBenh)\
    .join(KhamBenh, PhieuKhamBenh.id_KhamBenh==KhamBenh.id_BenhNhan)\
    .filter(KhamBenh.ngayKham==date).first()


print(a[0])