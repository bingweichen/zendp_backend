#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : model.py
@Time    : 2021/10/12 5:22 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 版块
"""


import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

from common.base_model import BaseModel, BasicModelMixin
from exts import db
from common import GlobalConstant


class Comment(BasicModelMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    # 创建者
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship("User")

    # 评论对象
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))

    # 描述（短）
    desc = db.Column(db.String(500))

    # 评分 10分制 5星
    rate = db.Column(db.Float, default=0)

