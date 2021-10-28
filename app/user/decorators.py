#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : decorators.py
@Time    : 2020/11/5 9:01 AM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""
from flask import g
from flask import request
from functools import wraps

from app.user.model import User
from app.user.service import get_current_user_id
from common.errors import (TokenBlackListedError,
                           ExpiredSignatureError,
                           InvalidTokenError,
                           TokenMissedError,
                           UserDoesNotExistError,
                           PermissionDeniedDataAccessException
                           )
from common.responses import unauthorized


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            # save user information to flask g variable
            g.user_id = get_current_user_id(request)
            return func(*args, **kwargs)
        except TokenMissedError as e:
            return unauthorized(e.message)
        except TokenBlackListedError as e:
            return unauthorized(e.message)
        except ExpiredSignatureError:
            return unauthorized('Token is expired, please try to login again!')
        except InvalidTokenError:
            return unauthorized('Invalid token, please try to login again!')
        except UserDoesNotExistError as e:
            return unauthorized(e.message)

    return decorated


def permission_can(current_user, permission):
    """
    检测用户是否有特定权限
    :param current_user
    :param permission
    :return:
    """
    roles = current_user.roles
    # roles 中有一个有 permissions
    for role in roles:
        if (role.permissions & permission) == permission:
            return True
    return False

    # 或者 permissions 求和
    # all_role_permissions = 0
    # for role in roles:
    #     all_role_permissions = all_role_permissions | role.permissions
    # return (all_role_permissions & permission) == permission

    # return (role.permissions & permission) == permission


def permission_required(permission):
    """
    权限认证装饰器
    :param permission:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = User.query.filter_by(id=g.user_id).first()
            if permission_can(current_user, permission):
                return f(*args, **kwargs)
            else:
                raise PermissionDeniedDataAccessException

        return decorated_function

    return decorator


def check_permission(permission):
    """
    权限认证函数
    :param permission:
    :type permission:
    :return:
    :rtype:
    """
    current_user = User.query.filter_by(id=g.user_id).first()
    if not permission_can(current_user, permission):
        raise PermissionDeniedDataAccessException
