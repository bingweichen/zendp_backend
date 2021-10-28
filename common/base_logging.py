#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : base_logging.py
@Time    : 2021/1/21 10:47 AM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""

import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler


class MyLogging():

    def __init__(self, log_name='', file_name='error'):
        self.logger = logging.getLogger(f'INTEL{log_name}')
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.check_root_dir()
        self.set_log_level(file_name)
        self.formatter = logging.Formatter(
            f'|{log_name}| %(asctime)s |%(levelname)s| [pathname:%(pathname)s] | '
            f'[funcName:%(funcName)s] [line:%(lineno)d] %(message)s')
        file_handler = TimedRotatingFileHandler(filename=f'{self.base_dir}/logs/{file_name}.log', when='w0',
                                                backupCount=30)
        # 日志保留30天，每周一自动切割
        file_handler.suffix = "%Y-%m-%d.log"
        # extMatch是编译好正则表达式，用于匹配日志文件名后缀
        # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        console = logging.StreamHandler()
        console.setFormatter(self.formatter)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(console)
        self.logger.addHandler(file_handler)

    def set_log_level(self, log_level):

        if log_level == 'error':
            self.logger.setLevel(logging.ERROR)
        elif log_level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def check_root_dir(self):
        path = f'{self.base_dir}/logs'
        if not os.path.exists(path):
            os.makedirs(path)


my_request_log = MyLogging(log_name='REQUEST', file_name='requests')
my_info_log = MyLogging(log_name='INFO', file_name='info')
my_error_log = MyLogging(log_name='ERROR', file_name='error')
