#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : __init__.py
@Time    : 2020/9/18 7:52 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""
import os

from app import create_app, make_celery

config_name = os.getenv('FLASK_ENV') or 'default'
# app = create_app(config_name)
# app = create_app('online_test')
app = create_app('production')

print("config_name", config_name)
print('app.name', app.name)

celery = make_celery(app)
