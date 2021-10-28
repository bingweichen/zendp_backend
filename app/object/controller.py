#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : controller.py
@Time    : 2021/10/12 7:14 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 创建词条，搜索词条，修改词条
"""

from flask import g
from flask_restplus import Resource, Namespace, fields, marshal, reqparse

from app.object.model import Object
from app.object.service import Service as ObjectService
from app.user.controller import user_model
from app.user.decorators import token_required
from common.decorators import catch_error
from common.responses import created, ok
from app.category.controller import category_model
from app.category.service import Service as CategoryService

api = Namespace('object', path='/object')

object_model = api.model('object', {
    'id': fields.String(description='object id'),
    'name': fields.String(description='object username'),
    'desc': fields.String(description='object desc'),
    'detail': fields.String(description='object detail'),
    'creator': fields.Nested(user_model),
    'rate': fields.Float(),
    'category': fields.Nested(category_model),

})

objects_paginate_model = api.model('paginate', {
    "pages": fields.Integer(),
    "page": fields.Integer(),
    "per_page": fields.Integer(),
    "total": fields.Integer(),
    "items": fields.Nested(object_model)
})


@api.route('/objects')
class ObjectsResource(Resource):
    @catch_error
    @api.response(201, 'object successfully created.')
    @token_required
    def post(self):
        """创建词条"""
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True, help='name')
        parser.add_argument('category_name', required=True, help='category_name')
        parser.add_argument('desc')
        parser.add_argument('detail')
        parser.add_argument('image_url')
        parser.add_argument('tags', type=str, help='标签', action='append')
        args = parser.parse_args()

        # 创建
        new_object = ObjectService.create_object(current_user_id=g.user_id, **args)

        return created(
            data=marshal(new_object, object_model),
            message='create object success')

    @catch_error
    def get(self):
        """搜索词条 分页排序筛选"""
        parser = reqparse.RequestParser()

        # 当 category 存在时，返回单一版块。当不存在时，返回所有版块，并统计每个版块条目个数
        parser.add_argument('category_name', help='category_name')

        parser.add_argument('search_str', help='search_str')
        parser.add_argument('current_page', type=int, default=1, help='current_page')
        parser.add_argument('per_page', type=int, choices=[2, 5, 10, 20, 40], default=20, help='per_page')

        parser.add_argument('sorted_by', type=str, choices=[
            'name', 'create_datetime', 'rate', 'trend'
        ], default='rate', help='sorted_by')

        parser.add_argument('sorted_by_type', type=str, choices=['desc', 'asc'], default='desc', help='sorted_by_type')

        args = parser.parse_args()

        object_query = Object.query

        if args.get('category_name'):
            object_query = object_query.filter_by(
                category_id=CategoryService.get_category_id_by_category_name(args.get('category_name')))

        # 搜索 本表筛选
        if args.get('search_str'):
            object_query = object_query \
                .filter(Object.name.like("%" + args.get('search_str') + "%"))

        objects_pagination = object_query \
            .filter_by() \
            .paginate(page=args.get('current_page'), per_page=args.get('per_page'))

        for row in objects_pagination.items:
            rate = ObjectService.calculate_rate(row.id)
            row.rate = rate

        return ok(data=marshal(objects_pagination, objects_paginate_model),
                  message='get objects success')


@api.route('/objects/<int:object_id>')
class ObjectResource(Resource):
    @catch_error
    def get(self, object_id):
        old_object = Object.query.filter_by(id=object_id).first()

        rate = ObjectService.calculate_rate(object_id)
        old_object.rate = rate

        return ok(
            data=marshal(old_object, object_model),
            message='get object success'
        )

    @catch_error
    @token_required
    def put(self, object_id):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True, help='name')
        parser.add_argument('category_name', required=True, help='category_name')
        parser.add_argument('desc')
        parser.add_argument('detail')
        parser.add_argument('image_url')
        parser.add_argument('tags', type=str, help='标签', action='append')
        args = parser.parse_args()

        # 创建
        new_object = ObjectService.update_object(g.user_id, object_id, **args)
        return ok(data=marshal(new_object, object_model), message="update success")
