""""""
import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

from common.base_model import BaseModel, BasicModelMixin
from exts import db
from common import GlobalConstant


class User(BasicModelMixin, db.Model, BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(GlobalConstant.middle_db_string_len), unique=True, nullable=False)
    nickname = db.Column(db.String(GlobalConstant.middle_db_string_len))
    phone = db.Column(db.NUMERIC, unique=True, nullable=True)
    email = db.Column(db.String(GlobalConstant.middle_db_string_len), unique=True, nullable=True)
    password_hash = db.Column(db.String(GlobalConstant.long_db_string_len))
    wechat_id = db.Column(db.String(GlobalConstant.long_db_string_len))
    identity = db.Column(db.String(GlobalConstant.middle_db_string_len), unique=True, nullable=True)  # 身份证号

    # 登录信息
    last_login_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login_ip = db.Column(db.String(GlobalConstant.long_db_string_len))


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User '{self.username}'>"


class BlackList(BasicModelMixin, db.Model, BaseModel):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<id: token: {self.token}'

    @staticmethod
    def check_blacklist(token):
        res = BlackList.query.filter_by(token=str(token)).first()
        return True if res else False




