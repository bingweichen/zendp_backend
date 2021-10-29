#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : service.py
@Time    : 2021/10/12 7:02 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""
from app.category.model import Category

from common import errors
from common.mixins import DictMixin


class Business:
    @staticmethod
    def create_category(**kwargs):
        new_category = DictMixin.from_dict(Category, kwargs)
        result = new_category.add()
        if result:
            raise errors.CreateFailureException(error_msg=result)
        return new_category


class Service:

    @staticmethod
    def init():
        Business.create_category(name='电影', desc='电影评论')
        Business.create_category(name='音乐', desc='音乐评论')
        Business.create_category(name='游戏', desc='游戏评论')
        Business.create_category(name='租房中介', desc='租房中介评论')
        Business.create_category(name='留学中介', desc='留学中介评论')
        Business.create_category(name='旅游地点', desc='旅游地点评论')
        Business.create_category(name='导师', desc='导师评论')
        Business.create_category(name='公司', desc='公司评论')

    @staticmethod
    def get_category_id_by_category_name(category_name):
        return Category.query.filter_by(name=category_name).first().id


if __name__ == "__main__":
    from app import create_app

    # app = create_app("default")
    # app = create_app("online_test")
    app = create_app("production")
    with app.app_context():
        Service.init()
