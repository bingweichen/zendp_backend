#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'chenbingwei'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    username = "xxx"
    password = "xxx"
    hostname = "localhost"
    port = 5432
    db_name = "zendp_dev"
    DATABASE_URI = 'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'.format(
        username=username, password=password, hostname=hostname, port=port, db_name=db_name)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    # REDIS_URL = "redis://:@localhost:6379/0"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class UnitTestConfig(Config):
    DEBUG = True
    username = "xxx"
    password = "xxx"
    hostname = "localhost"
    port = 5432
    db_name = "zendp_test"
    DATABASE_URI = 'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'.format(
        username=username, password=password, hostname=hostname, port=port, db_name=db_name)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL') or DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOSTNAME = 'localhost:5000/api'
    # REDIS_URL = "redis://:@localhost:6379/0"


class OnlineTestConfig(Config):
    DEBUG = False
    username = "xxx"
    password = "xxx"
    hostname = "xxx.xx.xxx.xxx"
    port = 5432
    db_name = "zendp_online_test"
    DATABASE_URI = 'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'.format(
        username=username, password=password, hostname=hostname, port=port, db_name=db_name)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'


class ProductionConfig(Config):
    DEBUG = False
    username = "xxx"
    password = "xxx"
    hostname = "xxx.xx.xxx.xxx"
    port = 5432
    db_name = "zendp_prod_10_20"  # "microerp_prod_5_15"
    DATABASE_URI = 'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'.format(
        username=username, password=password, hostname=hostname, port=port, db_name=db_name)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


config = {
    'default': DevelopmentConfig,

    'development': DevelopmentConfig,
    'testing': UnitTestConfig,
    'online_test': OnlineTestConfig,
    'production': ProductionConfig
}
