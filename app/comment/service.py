#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : service.py
@Time    : 2021/10/12 8:08 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""

from app.comment.model import Comment
from common import errors
from common.errors import (InvalidTokenError
                           )
from common.mixins import DictMixin


class Business:
    @staticmethod
    def create_object(current_user_id, **kwargs):
        new_object = DictMixin.from_dict(Comment, kwargs)
        new_object.creator_id = current_user_id
        result = new_object.add()
        if result:
            raise errors.CreateFailureException(error_msg=result)
        return new_object

    @staticmethod
    def update_object(old_object, **kwargs):
        new_object = DictMixin.from_dict(old_object, kwargs)
        result = new_object.update()
        if result:
            raise errors.DbCommitFailureException(result)
        return new_object


class Service:
    @staticmethod
    def create_comment(**kwargs):
        Business.create_object(**kwargs)

    @staticmethod
    def update_object(current_user_id, object_id, **kwargs):
        # 检查权限
        old_object = Comment.query.filter_by(id=object_id)
        if old_object.creator_id != current_user_id:
            raise InvalidTokenError

        return Business.update_object(old_object,  **kwargs)


