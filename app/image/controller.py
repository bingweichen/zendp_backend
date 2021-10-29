# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
1. 上传图片，获取图片url
2. 将图片存入对应object的 image_url

3. 通过 image_url 获取图片
"""

import uuid
from flask import current_app, Response, url_for
from flask import g
from flask import request
from flask import safe_join, send_file
from flask_restplus import Resource, Namespace, fields, marshal

from app.image.model import Image
from app.image.service import Service as ImageService
from common.decorators import catch_error
from common.responses import ok, bad_request, not_found
from config import config
# from app.user.model import Permissions
from app.user.decorators import token_required, permission_required


api = Namespace('image', path='/image')
image_model = api.model('image', {
    'id': fields.Integer(),
    'name': fields.String(),
    'image_file_path': fields.String(),
    'url': fields.String(),
    "create_datetime": fields.DateTime(description='创建时间'),
    "notes": fields.String(description='备注'),
    'is_active': fields.Boolean()
})

image_paginate_model = api.model('paginate', {
    "pages": fields.Integer(),
    "page": fields.Integer(),
    "per_page": fields.Integer(),
    "total": fields.Integer(),
    "items": fields.Nested(image_model)
})

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/images')
class ImagesResource(Resource):
    """Shop Resource"""

    # @token_required  # 需要放最外面
    # @catch_error
    # def get(self):
    #     """获取所有 image"""
    #     parser = api.parser()
    #     parser.add_argument('name', type=str, help='类别名称模糊匹配')
    #     parser.add_argument('current_page', type=int, default=1, help='current_page')
    #     parser.add_argument('per_page', type=int, choices=[2, 5, 10, 20, 40], default=20, help='per_page')
    #     parser.add_argument('is_active', type=str, choices=["false", "true", None], default=None, help='is_active')
    #     parser.add_argument('sorted_by',
    #                         type=str, choices=['name', 'create_datetime'], default='create_datetime', help='sorted_by')
    #     parser.add_argument('sorted_by_type', type=str, choices=['desc', 'asc'], default='desc', help='')
    #     args = parser.parse_args()
    #     filter_args = {}
    #     image_query = Image.query
    #
    #     # 本表筛选
    #     if args.get('name'):
    #         image_query = image_query \
    #             .filter(Image.name.like("%" + args.get('name') + "%"))
    #     if args.get('is_active'):
    #         filter_args['is_active'] = args.get('is_active')
    #     image_query = image_query.filter_by(**filter_args)
    #
    #     # 排序
    #     if args.get("sorted_by"):
    #         if args.get("sorted_by") == 'name':
    #             image_query = image_query.order_by(
    #                 Image.name.asc() if args.get('sorted_by_type') == 'asc' else Image.name.desc())
    #         elif args.get("sorted_by") == 'create_datetime':
    #             image_query = image_query.order_by(
    #                 Image.create_datetime.asc() if args.get(
    #                     'sorted_by_type') == 'asc' else Image.create_datetime.desc())
    #     # 分页
    #     image_pagination = image_query.paginate(page=args['current_page'], per_page=args['per_page'])
    #     return ok(data=marshal(image_pagination, image_paginate_model),
    #               message='Get image success')

    @token_required
    @catch_error
    # @permission_required(Permissions.IMAGE)
    def post(self):
        """导入 image"""
        image_file_path = "image/files/images_{}.png".format(str(uuid.uuid1()))
        full_image_file_path = safe_join(current_app.root_path, image_file_path)
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(full_image_file_path)
            # 在数据库记一笔
            new_image = ImageService.create(
                g.user_id,
                name=file.filename,
                image_file_path=image_file_path)

            url_mapping = {
                'development': 'http://localhost:5000/api/image/images',
                # 'online_test': 'http://test.jxcjxc.com/api/image/images',
                'production': 'http://www.zendp.com/api/image/images'
            }

            new_image.url = '{}/{}'.format(
                url_mapping[current_app.config.get("ENV")],
                str(new_image.id))
            new_image.update()
            return ok(data=marshal(new_image, image_model), message="create image success")
        else:
            return bad_request(message='wrong file or file type')


@api.route('/images/<int:image_id>')
class ImageResource(Resource):
    """ localhost:5000/api/image/images/1"""

    # @token_required
    @catch_error
    def get(self, image_id):
        image = Image.query.filter_by(id=image_id).first()
        if image:
            image_file_path = safe_join(
                current_app.root_path, image.image_file_path)

            with open(image_file_path, 'rb') as f:
                image = f.read()
                resp = Response(image, mimetype="image/jpg")
                return resp
        else:
            return not_found('找不到图片')

    # @token_required
    # @catch_error
    # # @permission_required(Permissions.IMAGE)
    # def put(self, image_id):
    #     parser = api.parser()
    #     parser.add_argument('name', type=str, help='名称')
    #     parser.add_argument('is_active', type=bool, choices=[False, True], help='is_active')
    #     parser.add_argument('notes', type=str, help='备注')
    #     args = parser.parse_args()
    #     image = ImageService.update_service(image_id, **args)
    #     return ok(data=marshal(image, image_model), message="update success")
    #
    # @token_required
    # @catch_error
    # # @permission_required(Permissions.IMAGE)
    # def delete(self, image_id):
    #     """删除warehouse"""
    #     del_image = ImageService.delete(image_id)
    #     return ok(data='', message="delete success")
