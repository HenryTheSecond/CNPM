from flask_admin.contrib.sqla import ModelView
from my_app.models import *
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from my_app import admin
from sqlalchemy import insert, func, extract

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_Id == 1

class BenhNhanView(AuthenticatedView):
    can_export = True
    column_searchable_list = ("ten", "soDT")
    column_filters = (BenhNhan.ten, BenhNhan.soDT)


class KhamBenhView(AuthenticatedView):
    can_export = True
    column_searchable_list = ("ngayKham", KhamBenh.id_BenhNhan)


class BacSiView(AuthenticatedView):
    pass

class BenhView(AuthenticatedView):
    pass

class CachDungView(AuthenticatedView):
    pass

class ChiTietHoaDonView(AuthenticatedView):
    pass

class DangKyOnlineView(AuthenticatedView):
    can_create = False

class DonThuocView(AuthenticatedView):
   can_create = True;


class DonViView(AuthenticatedView):
    pass

class HoaDonView(AuthenticatedView):
    pass

class PhieuKhamBenhView(AuthenticatedView):
    pass

class RoleView(AuthenticatedView):
    pass

class SoBenhNhanView(AuthenticatedView):
    pass

class TamThoiLuuTruView(AuthenticatedView):
    pass

class ThuocView(AuthenticatedView):
    pass

class TienKhamView(AuthenticatedView):
    pass

class UserView(AuthenticatedView):
    pass

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/login")

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose("/")
    def index(self):
        doanh_thu_theo_thang = db.session.query(extract('month', KhamBenh.ngayKham), func.sum(HoaDon.total)).join(
            HoaDon, KhamBenh.id == HoaDon.id_KhamBenh). \
            filter(extract('year', KhamBenh.ngayKham) == datetime.now().year).group_by(
            extract('month', KhamBenh.ngayKham)).all()
        return self.render("admin/stats.html", doanh_thu_theo_thang=doanh_thu_theo_thang)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_Id == 1

class RegisterView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/register.html")


admin.add_view(DangKyOnlineView(DangKyOnline, db.session , name="????ng K?? Online"))
admin.add_view(TamThoiLuuTruView(TamThoiLuuTru, db.session , name="L??u Tr??? T???m"))
admin.add_view(SoBenhNhanView(SoBenhNhan, db.session, name="S??? L?????ng B???nh Nh??n 1 Ng??y"))
admin.add_view(BenhNhanView(BenhNhan, db.session, name="B???nh Nh??n"))
admin.add_view(KhamBenhView(KhamBenh, db.session, name="Kh??m B???nh"))
admin.add_view(BenhView(Benh, db.session , name="B???nh"))
admin.add_view(PhieuKhamBenhView(PhieuKhamBenh, db.session, name="Phi???u Kh??m B???nh"))
#admin.add_view(DonThuocView(DonThuoc, db.session , name="????n Thu???c"))
#admin.add_view(ChiTietHoaDonView(ChiTietHoaDon, db.session , name="Chi Ti???t H??a ????n"))
admin.add_view(HoaDonView(HoaDon, db.session , name="H??a ????n"))
#admin.add_view(BacSiView(BacSi, db.session, name="B??c S??"))
admin.add_view(ThuocView(Thuoc, db.session , name="Thu???c"))
admin.add_view(CachDungView(CachDung, db.session , name="C??ch D??ng"))
admin.add_view(DonViView(DonVi, db.session , name="????n V???"))
#admin.add_view(RoleView(Role, db.session , name="Role"))
admin.add_view(TienKhamView(TienKham, db.session , name="Ti???n Kh??m B???nh"))
admin.add_view(StatsView(name="Th???ng K??"))
admin.add_view(UserView(User, db.session, name="User"))
admin.add_view(RegisterView(name="????ng k??"))
admin.add_view(LogoutView(name="????ng xu???t"))