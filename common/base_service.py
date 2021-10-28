#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf8')


class BaseService:
    def __init__(self, cls):
        self.cls = cls

    def get_all(self):
        return self.cls.query.filter_by().all()

    def get_all_json(self):
        objs_json = []
        objects = self.get_all()
        for obj in objects:
            obj_dict = obj.as_dict()
            objs_json.append(obj_dict)
        return objs_json


class RedisService:
    @staticmethod
    def set_phone_captcha(phone, captcha):
        redis_db.set(phone, captcha)
        redis_db.expire(phone, 600)  # 设置过期时间，10分钟

    @staticmethod
    def verify_phone_captcha(phone, captcha):
        # 当拿不到 phone 这个key的时候
        if not redis_db.get(phone):
            return False
        value = redis_db.get(phone).decode('utf-8')
        if captcha == value:
            return True
        return False
