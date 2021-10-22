from models import *
from datetime import datetime
from sqlalchemy import func
from my_app import db

date = datetime(year=2021, month=10, day=22)

(db.session.query(func.max(HoaDon.total)).filter().first())
