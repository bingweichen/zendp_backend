#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : exts.py
@Time    : 2019/11/15 3:36 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""

from flask import g
from flask_sqlalchemy import SQLAlchemy, BaseQuery


class Query(BaseQuery):
    def filter_by_company_id(self, **kwargs):
        if 'company_id' not in kwargs.keys():
            kwargs['company_id'] = g.company_id
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)
