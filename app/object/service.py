#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : service.py
@Time    : 2021/10/12 7:15 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""

from app.object.model import Object
from common import errors
from common.errors import (InvalidTokenError
                           )
from common.mixins import DictMixin
from app.comment.model import Comment
from sqlalchemy import func
from app.category.model import Category


class Business:
    @staticmethod
    def create_object(current_user_id, **kwargs):
        new_object = DictMixin.from_dict(Object, kwargs)
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
    def create_object(category_name, **kwargs):
        # 取出category name, 获取category_id
        category = Category.query.filter_by(name=category_name).first()
        return Business.create_object(category_id=category.id, **kwargs)

    @staticmethod
    def update_object(current_user_id, object_id, category_name, **kwargs):
        # 检查权限
        old_object = Object.query.filter_by(id=object_id).first()
        if old_object.creator_id != current_user_id:
            raise InvalidTokenError

        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            return Business.update_object(old_object, category_id=category.id, **kwargs)

        return Business.update_object(old_object,  **kwargs)

    @staticmethod
    def calculate_rate(object_id):
        comments = Comment.query.filter_by(object_id=object_id).all()
        score = 0
        num = 0
        for comment in comments:
            score += comment.rate
            num += 1
        if num == 0:
            return 0
        # score = Comment.query(func.avg(Comment.rate)).filter(Object.id == object_id).scalar()
        return score/num
