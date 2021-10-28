#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : controller.py
@Time    : 2021/10/12 7:10 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 获取版块列表
"""

from flask_restplus import Resource, Namespace, fields, marshal, reqparse

from app.category.model import Category
from common.decorators import catch_error
from common.responses import ok

api = Namespace('category', path='/category')

category_model = api.model('category', {
    'id': fields.String(description='category id'),
    'name': fields.String(description='category desc'),
})

categories_paginate_model = api.model('paginate', {
    "pages": fields.Integer(),
    "page": fields.Integer(),
    "per_page": fields.Integer(),
    "total": fields.Integer(),
    "items": fields.Nested(category_model)
})


@api.route('/categories')
class CommentsResource(Resource):
    @catch_error
    def get(self):
        """获取版块列表"""
        parser = reqparse.RequestParser()
        parser.add_argument('object_id', required=True, help='object_id')

        parser.add_argument('current_page', type=int, default=1, help='current_page')
        parser.add_argument('per_page', type=int, choices=[2, 5, 10, 20, 40], default=20, help='per_page')

        args = parser.parse_args()

        object_query = Category.query

        objects_pagination = object_query \
            .filter_by() \
            .paginate(page=args.get('current_page'), per_page=args.get('per_page'))

        return ok(data=marshal(objects_pagination, categories_paginate_model),
                  message='Get category success')
