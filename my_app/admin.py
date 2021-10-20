from flask_admin.contrib.sqla import ModelView
from my_app.models import BenhNhan, KhamBenh
from my_app import db, admin
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect

class AuthenticatedView(ModelView):
    pass

class BenhNhanView(AuthenticatedView):
    can_export = True
    column_searchable_list = ("ten", "soDT")

class KhamBenhView(AuthenticatedView):
    can_export = True
    column_searchable_list = ("ngayKham", KhamBenh.id_BenhNhan)

admin.add_view(BenhNhanView(BenhNhan, db.session, name="Bệnh Nhân"))
admin.add_view(KhamBenhView(KhamBenh, db.session, name="Khám Bệnh"))