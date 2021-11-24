from models import *
from datetime import datetime
from sqlalchemy import func, cast, Date
from my_app import db
import hmac
import hashlib
import requests
from twilio.rest import Client

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

'''dang_ky = DangKyOnline(id_BenhNhan=int(1), soDT='1234', ngayDangKy=datetime.now(),
                                   ngayKhamDangKy=datetime.now(), isKhamLanDau=True)

db.session.add(dang_ky)
db.session.commit()
print(dang_ky.id)'''


'''data = {
            "partnerCode": "MOMOFIF820211121",
            "partnerName" : "Tuyen",
            "storeId" : "Tuyen",
            "requestType": "captureWallet",
            "ipnUrl": "voz.vn",
            "redirectUrl": "voz.vn",
            "orderId": "tuyen1637716747768",
            "amount": "1000",
            "lang":  "en",
            "autoCapture": False,
            "orderInfo": "Thanh toán qua ví MoMo",
            "requestId": "tuyen1637716747768",
            "extraData": "",
            "signature": "9998a19535d91d8b03ea026b06c31ebf13289dcded222fd5af51b19fdbd17b81"
}
r = requests.post(url='https://test-payment.momo.vn/v2/gateway/api/create',json=data, headers={"Content-Type": "application/json; charset=UTF-8"})
print(r.json())'''


'''data = "accessKey=RCmyRRu3ONRNC9xm&amount=1000&extraData=&ipnUrl=http://127.0.0.1:5000/cashier&orderId=" + "1" + "&orderInfo=Thanh toán qua ví MoMo&partnerCode=MOMOFIF820211121&redirectUrl=http://127.0.0.1:5000/cashier&requestId=" + "1" + "&requestType=captureWallet"
signature = hmac.new(b"srorZC05FI40gRaEPYCMJjFKDGjtf4BM", data.encode(), hashlib.sha256).hexdigest()
print(signature)'''


client = Client("AC2de7639eaf115bcb2195774eb91a3b6f", "cf3786653d036cb8996ddb8085e22b5d")
client.messages.create(to="+840964147757", from_="+14422281058", body="Hello world")