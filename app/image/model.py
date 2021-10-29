#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.base_model import BaseModel, BasicModelMixin
from exts import db
from common import GlobalConstant


class Image(BasicModelMixin, db.Model, BaseModel):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(GlobalConstant.middle_db_string_len))
    image_file_path = db.Column(db.String(GlobalConstant.long_db_string_len), nullable=False)
    url = db.Column(db.String(GlobalConstant.long_db_string_len))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))



