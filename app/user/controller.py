#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from flask import g
from flask_restplus import Resource, Namespace, fields, marshal, reqparse

from app.user.decorators import token_required, permission_required
from app.user.model import User
from app.user.service import Service as UserService
from common import errors
from common.base_service import RedisService
from common.decorators import arguments_parser, catch_error
from common.responses import created, ok

api = Namespace('user', path='/user')

login_model = api.model('login', {
    'username': fields.String(required=True, description='user username'),
    'password': fields.String(required=True, description='user password '),
})

user_model = api.model('user', {
    'id': fields.String(description='user id'),
    'username': fields.String(description='user username'),
    "nickname": fields.String(description='user nickname'),
    "phone": fields.Integer(description='phone'),
    "email": fields.String(description='email'),
    "notes": fields.String(description='notes'),
    "wechat_id": fields.String(description='wechat_id'),
    "identity": fields.String(description='identity'),
    "is_admin": fields.Boolean(description='is_admin'),

})

paginate_model = api.model('paginate', {
    "pages": fields.Integer(),
    "page": fields.Integer(),
    "per_page": fields.Integer(),
    "total": fields.Integer(),
    "items": fields.Nested(user_model)
})


@api.route('/auth/register')
class RegisterResource(Resource):
    @catch_error
    @api.response(201, 'Admin successfully created.')
    @api.doc('register')
    def post(self):
        """管理员注册"""
        parser = reqparse.RequestParser()
        # parser.add_argument('company_name', help='company_name')
        parser.add_argument('username', help='username')
        parser.add_argument('password', required=True, help='password')
        parser.add_argument('phone', required=True, help='phone')
        parser.add_argument('email', help='email')

        parser.add_argument('captcha', required=True, help='captcha')
        args = parser.parse_args()

        # 手机号，验证码校验
        if not RedisService.verify_phone_captcha(args.get("phone"), args.get("captcha")):
            raise errors.PhoneCaptchaNotMatchException

        # 默认生成 用户名
        if not args.get("username"):
            args['username'] = "默认用户名{}".format(uuid.uuid4())

        # 创建 用户
        new_user = UserService.create_user(**args)

        # 获取token
        token, user = UserService.login(username=args.get("username"), password=args.get("password"))

        return created(data={
            "Authorization": token,
            'user': marshal(new_user, user_model)
        }, message='Successfully registered!')


@api.route('/auth/reset_password')
class ResetPassword(Resource):
    @catch_error
    def post(self):
        """重置密码"""
        parser = reqparse.RequestParser()
        parser.add_argument('phone', required=True, help='phone')
        parser.add_argument('password', required=True, help='password')
        parser.add_argument('captcha', required=True, help='captcha')
        args = parser.parse_args()

        # 手机号
        user = User.query.filter_by(phone=args.get("phone")).first()
        if not user:
            raise errors.NotRegisterException()

        # 手机号，验证码校验
        if not RedisService.verify_phone_captcha(args.get("phone"), args.get("captcha")):
            raise errors.PhoneCaptchaNotMatchException

        new_user = UserService.reset_password(user, args.get("password"))

        # 获取token
        token, user = UserService.login(username=user.username, password=args.get("password"))

        return created(data={
            "Authorization": token,
            'user': marshal(new_user, user_model)
        }, message='Successfully reset password!')


@api.route('/auth/login')
class LoginResource(Resource):
    """User Login Resource"""

    @catch_error
    @api.doc(description='user login')
    @api.expect(login_model, validate=True)
    @arguments_parser
    def post(self):
        """用户名登录 手机号登陆"""
        data = g.args

        token, user = UserService.login(username=data.get("username"), password=data.get("password"))

        # 设置 g
        g.user_id = user.id
        # g.company_id = user.company_id

        return ok(data={
            "Authorization": token,
            "user": marshal(user, user_model),
        }, message="Successfully logged in")


@api.route('/auth/logout')
class LogoutResource(Resource):
    """
    Logout Resource
    """

    @api.doc(description='user logout')
    @token_required
    @catch_error
    def get(self):
        result = UserService.logout()
        return ok(result, 'Logout successfully!')


@api.route('/users/current_user')
class CurrentUserResource(Resource):
    @api.doc(description='get current_user')
    @token_required
    @catch_error
    def get(self):
        user = User.query.filter_by(id=g.user_id).first()

        return ok(data={
            **marshal(user, user_model),

        }, message='get current_user successfully')


@api.route('/users')
class UsersResource(Resource):
    @catch_error
    @token_required
    def get(self):
        """获取所有用户"""
        parser = reqparse.RequestParser()
        parser.add_argument('current_page', type=int, default=1, help='current_page')
        parser.add_argument('per_page', type=int, choices=[2, 5, 10, 20, 40], default=20, help='per_page')
        parser.add_argument('is_active', type=str, choices=["false", "true", None], default=None, help='is_active')
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('nickname', type=str, help='nickname')
        parser.add_argument('sorted_by', type=str, choices=[
            'username', 'nickname', 'create_datetime'
        ], default='create_datetime', help='sorted_by')
        parser.add_argument('sorted_by_type', type=str, choices=['desc', 'asc'], default='desc', help='')

        args = parser.parse_args()
        filter_args = {}
        user_query = User.query

        # 本表筛选
        if args.get("is_active"):
            filter_args['is_active'] = True if args.get("is_active") == 'true' else False
        if args.get('username'):
            user_query = user_query.filter(
                User.username.like("%" + args.get('username') + "%"))
        if args.get('nickname'):
            user_query = user_query.filter(
                User.nickname.like("%" + args.get('nickname') + "%"))
        user_query = user_query.filter_by_company_id(
            **filter_args
        )

        # 排序
        if args.get("sorted_by"):
            if args.get("sorted_by") == 'username':
                user_query = user_query.order_by(
                    User.username.asc() if args.get('sorted_by_type') == 'asc' else User.username.desc())
            elif args.get("sorted_by") == 'nickname':
                user_query = user_query.order_by(
                    User.nickname.asc() if args.get('sorted_by_type') == 'asc' else User.nickname.desc())
            elif args.get("sorted_by") == 'create_datetime':
                user_query = user_query.order_by(
                    User.create_datetime.asc() if args.get('sorted_by_type') == 'asc' else User.create_datetime.desc())

        # 删掉 order_by
        users_pagination = user_query.paginate(
            page=args['current_page'],
            per_page=args['per_page'])
        return ok(data=marshal(users_pagination, paginate_model), message='Get users success')


@api.response(404, 'User not found')
@api.route('/users/<int:user_id>')
class UserResource(Resource):
    @catch_error
    @token_required
    @api.marshal_with(user_model)
    def get(self, user_id):
        """获取单个用户"""
        return User.filter_by_company_id(id=user_id).first()

    @token_required
    @catch_error
    @api.marshal_with(user_model)
    @arguments_parser
    def put(self, user_id):
        """用户个人资料修改"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='username')
        parser.add_argument('nickname', help='nickname')
        parser.add_argument('password', help='password')
        parser.add_argument('phone', help='phone')
        parser.add_argument('email', help='email')
        parser.add_argument('notes', help='notes')
        parser.add_argument('wechat_id', help='wechat_id')
        parser.add_argument('identity', help='identity')
        parser.add_argument('is_active', type=bool, choices=(True, False), help='Bad choice: {error_msg}')  #
        parser.add_argument('join_date', type=str, help='入司时间')
        parser.add_argument('role_ids', type=int, help='role_ids', action='append', location='values')
        parser.add_argument('captcha', help='captcha')

        args = parser.parse_args()
        # 如果为空，则不要更新
        for key in list(args.keys()):
            if args.get(key) is None:
                del args[key]

        # 权限检查
        current_user = User.query.filter_by(id=g.user_id).first()

        if user_id != current_user.id:
            raise errors.PermissionDeniedDataAccessException

        # 如果更新手机号
        if args.get("phone"):
            user = User.query.filter_by(phone=args.get("phone")).first()
            if user:
                raise errors.PhoneNumberExistException

            # 手机号，验证码校验
            if not RedisService.verify_phone_captcha(args.get("phone"), args.get("captcha")):
                raise errors.PhoneCaptchaNotMatchException

        new_user = UserService.update_user(g.user_id, user_id, **args)
        return new_user

    # @catch_error
    # @token_required
    # def delete(self, user_id):
    #     """删除单个用户"""
    #     del_user = UserService.delete_user(user_id)
    #     return ok(data='', message="delete user success")


@api.route('/users/is_username_exist')
class IsUsernameExistResource(Resource):
    @catch_error
    @arguments_parser
    def get(self):
        result = UserService.is_username_exist(g.args["username"])
        return ok(data={"is_username_exist": result}, message="check finished")


@api.route('/users/is_phone_exist')
class IsPhoneExistResource(Resource):
    @catch_error
    @arguments_parser
    def get(self):
        result = UserService.is_phone_exist(g.args["phone"])
        return ok(data={"is_phone_exist": result}, message="check finished")


# 发送验证码
@api.route('/send_captcha')
class SendCaptchaResource(Resource):
    @catch_error
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, help='phone')
        args = parser.parse_args()
        phone = args.get('phone')
        UserService.send_captcha(phone)
        return ok(data={"phone": phone}, message="send captcha success")
