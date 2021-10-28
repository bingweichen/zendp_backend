#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : dao.py
@Time    : 2021/10/12 8:46 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 计算评分

计算评分 5分几个
"""

from flask_records.decorators import query

from common.base_dao import BaseDao


class ObjectDao(BaseDao):

    def __init__(self):
        super(ObjectDao, self).__init__()

    CALCULATE_RATE = """
        select rate, count from comment 
          where comment.object_id = :object_id
          group by comment.rate 
    
    """

    def calculate_rate(self, object_id):
        sql = self.CALCULATE_RATE

        @query(sql)
        def _get(object_id):
            pass
        return _get(object_id)


object_dao = ObjectDao()
