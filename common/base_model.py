import datetime
from flask import g
from sqlalchemy.exc import SQLAlchemyError

from exts import db


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason


class BaseModel:

    @classmethod
    def filter_by_company_id(cls, company_id=None, **kwargs):
        if not company_id:
            company_id = g.company_id
        return cls.query.filter_by(**kwargs, company_id=company_id)

    @classmethod
    def filter_by_company(cls, company_id=None, **kwargs):
        if not company_id:
            company_id = g.company_id
        return cls.filter_by(**kwargs, company_id=company_id)

    @classmethod
    def filter_company_id(cls, *args, company_id=None, **kwargs):
        if not company_id:
            company_id = g.company_id
        return cls.query.filter(*args, **kwargs, company_id=company_id)

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self):
        db.session.add(self)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self):
        db.session.delete(self)
        return session_commit()

    def add_or_update(self):
        db.session.add(self)
        return session_commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OwnerMixin(object):
    company_id = db.Column(db.String(50), nullable=False)


class TimestampMixin(object):
    create_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class NormalMixin(object):
    notes = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    is_delete = db.Column(db.Boolean, default=False)


# 删掉
class CommonModelMixin(OwnerMixin, TimestampMixin):
    notes = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    is_delete = db.Column(db.Boolean, default=False)


class BasicModelMixin(NormalMixin, TimestampMixin):
    pass
