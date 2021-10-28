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


class Category(BasicModelMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(GlobalConstant.middle_db_string_len), unique=True, nullable=False)

    # 描述（短）
    desc = db.Column(db.String(500))
