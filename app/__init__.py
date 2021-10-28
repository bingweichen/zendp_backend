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

import decimal
import json
from celery import Celery
from flask import Flask, Blueprint
from flask import current_app, make_response
from flask_cors import CORS
from flask_records import FlaskRecords
from flask_restplus import Api
from json import dumps

from app.user.controller import api as user_ns
from app.object.controller import api as object_ns
from app.comment.controller import api as comment_ns
from app.category.controller import api as category_ns

from config import config
from exts import db


blueprint = Blueprint('api', __name__)

AUTHORIZATIONS = {
    "Authorization": {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint, title='FLASK　RestPlus API Server', version='0.1',
    description='a boilerplate for flask restplus web service', prefix='/api',
    authorizations=AUTHORIZATIONS,
    security=list(AUTHORIZATIONS.keys())
)


# 配置 json encoder for decimal type
@api.representation('application/json')  # 指定响应形式对应的转换函数
def output_json(data, code, headers=None):
    """自定义json形式 https://blog.csdn.net/li944254211/article/details/109366048"""

    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            super(DecimalEncoder, self).default(o)

    # 根据flask内置配置, 进行格式处理(缩进/key是否排序等)
    settings = current_app.config.get('RESTFUL_JSON', {})

    # 字典转json字符串
    dumped = dumps(data, **settings, cls=DecimalEncoder) + "\n"

    # 构建响应对象
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


api.add_namespace(user_ns, path='/user')
api.add_namespace(object_ns, path='/object')
api.add_namespace(comment_ns, path='/comment')
api.add_namespace(category_ns, path='/category')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    FlaskRecords(app)
    CORS(app, supports_credentials=True)
    app.register_blueprint(blueprint)

    # # redis
    # redis_client.init_app(app)
    return app


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'],
                    include=['celery_tasks.tasks']
                    )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
