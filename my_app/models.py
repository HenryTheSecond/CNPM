from my_app import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

class Role(db.Model):
    #__tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenRole = Column(String(50))
    users = relationship("User", backref="role", lazy=True)

    def __str__(self):
        return self.tenRole


DonThuoc = db.Table("don_thuoc", db.Model.metadata,
                    Column("id_KhamBenh", Integer, ForeignKey("PhieuKhamBenh.id_KhamBenh"), primary_key=True),
                    Column("id_Thuoc", Integer, ForeignKey("Thuoc.id"), primary_key=True),
                    Column("soLuong", Integer),
                    Column("id_CachDung", Integer, ForeignKey("CachDung.id")))


ChiTietHoaDon = db.Table("chi_tiet_hoa_don", db.Model.metadata
                         ,Column("id_KhamBenh", Integer, ForeignKey("HoaDon.id_KhamBenh"), primary_key=True),
                         Column("id_Thuoc", Integer, ForeignKey("Thuoc.id"), primary_key=True),
                        Column("gia", Integer, nullable=False),
                            Column("soLuong", Integer, nullable=False))


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable= False)
    ten = Column(String(50), nullable=False)
    gioiTinh = Column(String(4))
    diaChi = Column(String(150))
    ngaySinh = Column(Date)
    soDT = Column(String(20))
    role_Id = Column(Integer, ForeignKey(Role.id), nullable=False)
    danhSachBacSi = relationship("BacSi", backref="thongTin", lazy=True, uselist=False)

    def __str__(self):
        return self.ten

class BacSi(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    danhSachPhieuKham = relationship("PhieuKhamBenh", backref="bacSi", lazy=True)

    def __str__(self):
        return "Id bác sĩ: " + str(self.id)

class Benh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    danhSachPhieuKham = relationship("PhieuKhamBenh", backref="benh", lazy=True)

    def __str__(self):
        return self.ten

class CachDung(db.Model):
    __tablename__ = "cach_dung"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    danhSachDonThuoc = relationship(DonThuoc, back_populates="cachDung", lazy=True)

    def __str__(self):
        return self.ten

class DonVi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    danhSachThuoc = relationship("Thuoc", backref="donVi", lazy=True)

    def __str__(self):
        return self.ten

class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    id_DonVi = Column(Integer, ForeignKey(DonVi.id), nullable=False)
    gia = Column(Float, nullable=False)
    danhSachHoaDon = relationship("HoaDon", secondary=ChiTietHoaDon, backref='thuoc', lazy='subquery')
    danhSachDonThuoc = relationship("PhieuKhamBenh",  secondary=DonThuoc, back_populates="thuoc", lazy='subquery')

    def __str__(self):
        return self.tenThuoc

class SoBenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    soLuong = Column(Integer, nullable=False)

    def __str__(self):
        return self.soLuong

class TienKham(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gia = Column(Float, nullable=False)

    def __str__(self):
        return self.gia

class BenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(60), nullable=False)
    gioiTinh = Column(String(4))
    diaChi = Column(String(150))
    ngaySinh = Column(Date)
    soDT = Column(String(20))
    cacLanKham = relationship("KhamBenh", backref="benhNhan", lazy=True)
    dangKyOnline = relationship("DangKyOnline", backref="benhNhan", lazy=True)

    def __str__(self):
        return self.ten

class KhamBenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    ngayKham = Column(DateTime, default=datetime.now())
    phieuKham = relationship("PhieuKhamBenh", backref="khamBenh", lazy=True, uselist=False)
    #donThuoc = relationship("DonThuoc", backref="khamBenh", lazy=True)
    #hoaDon = relationship("HoaDon", backref="khamBenh", lazy=True)

    def __str__(self):
        return self.benhNhan.ten + ", khám ngày:" + str(self.ngayKham)

class PhieuKhamBenh(db.Model):
    id_KhamBenh = Column(Integer, ForeignKey(KhamBenh.id), primary_key=True)
    trieuChung = Column(String(150))
    id_Benh = Column(Integer, ForeignKey(Benh.id))
    id_BacSi = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    hoaDon = relationship("HoaDon", backref="khamBenh", lazy=True, uselist=False)
    donThuoc = relationship("Thuoc",  secondary="DonThuoc", backref= "phieuKham", lazy='subquery')

    def __str__(self):
        return "Id khám bệnh: " + str(self.id_KhamBenh) + ", Id bệnh: " + str(self.id_Benh) + ", Id bác sĩ: " + str(self.id_BacSi)




class HoaDon(db.Model):
    id_KhamBenh = Column(Integer, ForeignKey(PhieuKhamBenh.id_KhamBenh), primary_key=True)
    total = Column(Float)
    danhSachChiTietThuoc = relationship("Thuoc", secondary="ChiTietHoaDon", backref="hoaDon", lazy='subquery')

    def __str__(self):
        return "Id phiếu khám bệnh: " + str(self.id_KhamBenh)




class DangKyOnline(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_BenhNhan = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    soDT = Column(String(20), nullable=False)
    ngayDangKy = Column(DateTime, default=datetime.now())
    ngayKhamDangKy = Column(DateTime, nullable=False)
    isKhamLanDau = Column(Boolean, default=False) # đánh dấu bệnh nhân đã từng khám ở bệnh viện
    tamThoiLuu = relationship("TamThoiLuuTru", backref="dangKyOnline", lazy=True, uselist=False)

    def __str__(self):
        return str(self.ngayKhamDangKy) + "---" + str(self.ngayDangKy)  + "---" + str(self.id_BenhNhan) + "---" + str(self.isKhamLanDau)

class TamThoiLuuTru(db.Model):
    id = Column(Integer, ForeignKey(DangKyOnline.id), nullable=False, primary_key=True)
    #soDT = Column(String(20), nullable=False)
    trangThai = Column(Boolean, default=False) # trangThai=False là người bệnh chưa thanh toán đăng ký
                                               # trangThai=True là người bệnh đã thanh toán nhưng đang chờ duyệt
    # nếu như bệnh nhân đang ở trong bảng TamThoiLuuTru nhưng trước đó đã từng đăng ký online thì sẽ lấy lần đăng ký
    # có thời gian đăng ký gần đây nhất
    def __str__(self):
        return "Id đăng ký onl: " + str(self.id) + ", trạng thái: " + str(self.trangThai)


if __name__ == "__main__":
    db.create_all()