#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import jwt
import random
from flask import request

from app.user.model import User, BlackList
from common import errors
from common.base_service import RedisService
from common.errors import (TokenBlackListedError,
                           ExpiredSignatureError,
                           InvalidTokenError,
                           TokenMissedError,
                           UserDoesNotExistError,
                           NotMatchOrUserDoesNotExistsError,
                           NotActiveUserException
                           )
from common.mixins import DictMixin
from config import Config
from common.utils import get_ip_address, check_phone_number
from app.sms.service import Service as SmsService


class Business:
    @staticmethod
    def create_user(**kwargs):
        # 判断用户名是否为手机号
        if check_phone_number(kwargs.get("username")):
            raise errors.UsernameFormatException

        new_user = DictMixin.from_dict(User, kwargs)
        new_user.password = kwargs.get('password')
        result = new_user.add()
        if result:
            raise errors.CreateFailureException(error_msg=result)
        return new_user



class Service:
    @staticmethod
    def create_user(**kwargs):
        """注册 主用户"""
        user = Business.create_user(
            **kwargs
        )
        return user

    @staticmethod
    def super_admin_check_password(password):
        super_admin = User.query.filter_by(username='super_admin_chenbingwei').first()
        if super_admin:
            return super_admin.check_password(password)
        return False

    @staticmethod
    def login(username, password):
        # 先拿用户名匹配手机号
        if check_phone_number(username):
            user = User.query.filter_by(phone=username).first()
        else:
            user = User.query.filter_by(username=username).first()

        if user:
            # 用户密码登录，或者超级管理员使用密码登录
            if user.check_password(password) or Service.super_admin_check_password(password):
                if not user.is_active:
                    raise NotActiveUserException()
                token = generate_token(user.id)
                last_login_ip = get_ip_address(request)
                last_login_time = datetime.datetime.utcnow()
                user.last_login_ip = last_login_ip
                user.last_login_time = last_login_time
                user.update()
                return token.decode('utf-8'), user
            else:
                raise NotMatchOrUserDoesNotExistsError

        else:
            raise NotMatchOrUserDoesNotExistsError

    @staticmethod
    def logout():
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.split(" ")[1] if authorization_header else ''
        if token:
            resp = decode_token(token)
            if not isinstance(resp, str):
                add_token_to_blacklist(token=token)
        else:
            raise InvalidTokenError

    @staticmethod
    def update_user(current_user_id, user_id, **kwargs):
        # 检查权限
        current_user = User.query.filter_by(id=current_user_id).first()
        # # 1. current_user不是admin， 且修改他人  不需要了
        if current_user_id != user_id:
            raise InvalidTokenError
        user = User.query.filter_by(id=user_id).first()

        # 如果更新用户名
        if kwargs.get("username"):
            # 检查用户名
            if check_phone_number(kwargs.get("username")):
                raise errors.UsernameFormatException

        new_user = DictMixin.from_dict(user, kwargs)
        if kwargs.get('password'):
            new_user.password = kwargs.get('password')

        # if kwargs.get('role_ids') is not None:
        #     role_ids = kwargs.pop('role_ids')
        #     RoleService.update_user2role(user_id, role_ids, company_id=user.company_id)

        result = new_user.update()
        if result:
            raise errors.DbCommitFailureException(result)
        return new_user

    @staticmethod
    def delete_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        # 只删除普通用户，无法删除管理员
        if user.is_admin:
            raise errors.AdminUserDeleteException(error_msg="admin user cannot be delete")
        result = user.delete()
        if result:
            raise errors.CreateFailureException(error_msg=result)
        return user

    @staticmethod
    def is_username_exist(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def is_phone_exist(phone):
        user = User.query.filter_by(phone=phone).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def send_captcha(phone):
        # 手机号码校验 (前端正则校验过，后端再校验一次)
        if not check_phone_number(phone):
            raise errors.PhoneNumberException
        # 生成验证码
        captcha = ''.join(random.sample('1234567890', 6))
        # redis 保存 手机号 验证码
        RedisService.set_phone_captcha(phone, captcha)
        # 发送短信
        response = SmsService.send_captcha_by_sms(phone, captcha)
        print("response", response)

    @staticmethod
    def reset_password(user, password):
        user.password = password
        user.update()
        return user

    @staticmethod
    def create_super_admin(password):
        Business.create_user(
            username='super_admin_chenbingwei',
            password=password
        )


def add_token_to_blacklist(token):
    blacklist = BlackList(token)
    blacklist.add()


def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY)
        is_blacklisted_token = BlackList.check_blacklist(token)
        if is_blacklisted_token:
            raise TokenBlackListedError
        else:
            return payload['sub']
    except ExpiredSignatureError:
        raise ExpiredSignatureError
    except InvalidTokenError:
        raise InvalidTokenError


def get_current_user_id(current_request):
    authorization_header = current_request.headers.get('Authorization')
    if authorization_header:
        if len(authorization_header.split(" ")) != 2:
            raise TokenMissedError
        token = authorization_header.split(" ")[1]
    else:
        raise TokenMissedError

    if token:
        user_id = decode_token(token)
        user = User.query.filter(User.id == user_id).first()
        if not user:
            raise UserDoesNotExistError
        return user.id
    else:
        raise InvalidTokenError


def check_permission(permissions, permission):
    return (permissions & permission) == permission


if __name__ == "__main__":
    from app import create_app

    app = create_app("default")
    # app = create_app("online_test")
    # app = create_app("production")
    with app.app_context():
        # Role.init_role()
        # update_default_print_setting()
        # Service.create_guest_user()
        Service.create_super_admin('')
        # _data = {
        #     "username": "默认管理员1",
        #     "password": "123456",
        #     "is_admin": True,
        # }
        # Service.register_company_user(_data)
        # Role.init_role()


