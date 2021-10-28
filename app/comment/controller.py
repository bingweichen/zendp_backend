#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : controller.py
@Time    : 2021/10/12 8:08 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 创建评论，获取词条评论，修改评论
"""

from flask_restplus import Resource, Namespace, fields, marshal, reqparse
from flask import g

from app.comment.model import Comment
from app.comment.service import Service as CommentService
from app.user.controller import user_model
from app.user.decorators import token_required
from common.decorators import catch_error
from common.responses import created, ok

api = Namespace('comment', path='/comment')

comment_model = api.model('comment', {
    'id': fields.String(description='comment id'),
    'desc': fields.String(description='comment desc'),
    'rate': fields.Integer(description='comment rate'),
    'creator': fields.Nested(user_model)
})

comments_paginate_model = api.model('paginate', {
    "pages": fields.Integer(),
    "page": fields.Integer(),
    "per_page": fields.Integer(),
    "total": fields.Integer(),
    "items": fields.Nested(comment_model)
})


@api.route('/comments')
class CommentsResource(Resource):
    @catch_error
    @api.response(201, 'comment successfully created.')
    @token_required
    def post(self):
        """创建评论"""
        parser = reqparse.RequestParser()

        parser.add_argument('object_id', required=True, help='object_id')
        parser.add_argument('desc')
        parser.add_argument('rate')
        args = parser.parse_args()

        # 创建
        new_object = CommentService.create_comment(current_user_id=g.user_id, **args)

        return created(
            data=marshal(new_object, comment_model),
            message='Successfully registered!')

    @catch_error
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('object_id', required=True, help='object_id')

        parser.add_argument('current_page', type=int, default=1, help='current_page')
        parser.add_argument('per_page', type=int, choices=[2, 5, 10, 20, 40], default=20, help='per_page')

        args = parser.parse_args()

        comment_query = Comment.query

        comments_pagination = comment_query \
            .filter_by(object_id=args.object_id) \
            .paginate(page=args.get('current_page'), per_page=args.get('per_page'))

        return ok(data=marshal(comments_pagination, comments_paginate_model),
                  message='get comments success')
