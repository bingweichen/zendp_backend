#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : model.py
@Time    : 2021/10/12 5:22 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""


import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

from common.base_model import BaseModel, BasicModelMixin
from exts import db
from common import GlobalConstant


class Object(BasicModelMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(GlobalConstant.middle_db_string_len), unique=True, nullable=False)

    # 类别
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category")

    # 描述（短）
    desc = db.Column(db.String(500))

    # 详情 （富文本）
    detail = db.Column(db.String(500))

    # 图片
    image_url = db.Column(db.String(GlobalConstant.long_db_string_len))

    # 创建者
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship("User")

    # 标签
    tags = db.Column(db.JSON)

    # 分数 rate_score 通过所有评价计算得到
    # @getattr
    # def rate_score(self):
    #     pass