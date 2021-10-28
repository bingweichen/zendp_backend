# import logging
import importlib
import json
import pandas as pd
import pickle
import re
from decimal import Decimal
from pypinyin import pinyin, Style

from common.mixins import DictMixin
from math import ceil
# is_dump = True
is_dump = False


# LOGGING_FILE = 'runserver.log'
# logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)


def custom_round(number, round_type='integer'):
    if round_type == 'integer':
        return float(Decimal(number).quantize(Decimal('0')))
    elif round_type == 'percentage':
        return float(Decimal(number).quantize(Decimal('0.00')))
    elif round_type == 'ultra_percentage':
        return float(Decimal(number).quantize(Decimal('0.0000')))


def dump_pickle(data, file_path):
    if is_dump:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def get_instance_of_attr(path):
    module, function = path.rsplit('.', maxsplit=1)
    module_instance = importlib.import_module(module)
    if hasattr(module_instance, function):
        return getattr(module_instance, function)
    else:
        raise AttributeError


def get_ip_address(request):
    if request.headers.get('X-Real-Ip'):
        return request.headers.get('X-Real-Ip')
    else:
        return request.remote_addr


def check_phone_number(phone):
    ret = re.match(r"^1[35678]\d{9}$", phone)
    if ret:
        return True
    return False


# 库存成本计算
def calculate_warehouse_record_price(before_num, before_price, add_num, add_price):
    # before_num 库存为负数
    if before_num < 0:
        return add_price
    # 防止 before_num + add_num = 0
    if add_num == 0:
        return before_price

    # 价格为空判断
    if not before_price:
        before_price = 0
    return (before_num * before_price + add_num * add_price) / (before_num + add_num)
    # return (before_num * float(before_price) + add_num * add_price) / (before_num + add_num)


# 库存成本回退计算
def calculate_warehouse_record_price_revoke(before_num, before_price, remove_num, remove_price):
    # 价格为空判断   100 2 120 2 = 110 /  110 * 4 - 120 * 2
    # 80 * 0 + 160 * 1 = 160  - 160 * 1
    if before_num == remove_num:
        return 0
    if not before_price:
        before_price = 0
    return (before_num * before_price - remove_num * remove_price) / (before_num - remove_num)


# 计算pages, 通过 total / per_page 向上取整
def get_pages(per_page, total):
    """The total number of pages"""
    if per_page == 0:
        pages = 0
    else:
        pages = int(ceil(total / float(per_page)))
    return pages


# 自定义序列化
def custom_marshal_pagination(pagination_data):
    list_data = [DictMixin.to_dict(ele.as_dict()) for ele in pagination_data.data]

    return {
        "pages": get_pages(per_page=pagination_data.page_size, total=pagination_data.total),
        "page": pagination_data.page,
        "per_page": pagination_data.page_size,
        "total": pagination_data.total,
        "items": list_data
    }


def custom_marshal_list(list_data):
    return [DictMixin.to_dict(ele.as_dict()) for ele in list_data]


class Utils(object):
    """
    convert records collection to dataframe
    """

    @staticmethod
    def get_dataframe(res):
        df = pd.DataFrame([DictMixin.to_dict(i.as_dict()) for i in res])
        return df

    """
    convert pandas dataframe to python list
    """

    @staticmethod
    def to_pylist(dataframe):
        columns = dataframe.columns.values.tolist()
        data_source = []
        for index, row in dataframe.iterrows():
            dic = {}
            for column in columns:
                dic[column] = row[column]
            data_source.append(dic)
        return data_source

    @staticmethod
    def dataframe2json(df):
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def json2dataframe(json_data):
        return pd.read_json(json.dumps(json_data), orient='records')

    @staticmethod
    def fill_df_nan(dataframe):
        # fill the nan value with none for json
        dataframe = dataframe.where(pd.notnull(dataframe), None)


#
# from Crypto import Random
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
# import base64
#
# private_key = """
# -----BEGIN RSA PRIVATE KEY-----
# MIICWwIBAAKBgQC85duhn+XToVi4LxZ2Ii+ux1ywbpOLZsw/6i2TvUGnaQStBohH
# ewTprh7lZj9ij980aS8ARh25pWeYTWpWg49oMtHGhIzFV2uws8fDtc5Hsfg12IO2
# gXBxWFPvFxCmJghl1iaEn9/We+uGtHgbs3NKj7KNI3hL+pOL6OAFEesBdQIDAQAB
# AoGABot1lJ/+99ol7MZqN3rvvqqBoktH1BNNDa8wwmb9mK32z4KObjZA8VJrF5+h
# 9T7u3i4BcYz8XVZHGevKEhKfgU7JbQTIdIf8+aTCFBfuAf8ff8ImdrfGQgut99EJ
# TVIjYviUUpxG3Q34Xel3DPve4yqGd6AbM+cyj+0EgDYZroECQQDQWfDVZMPpm7ec
# w/Z4bLoZI2+jF38Bg9++GKH66l/HmoEri6kEtImTc8m4rnVBI/flMhu1MpKnnD8H
# g3P3xuIdAkEA6BkAumomW8EOsPoVxQk/Jre82mCLRyRvHEJsVsy3oApnmf+qYgfT
# DW/vSRhxp4noOnowDP7FOslme4t6thz9OQJAHLuqmOMymW7eHYJw5R6pc3oNlUJS
# Q5U6L+8Zt47G8rH+ClFSV9HF/03CjfORPBCHyVXluFFnJDJKBvE79vm4iQJAH/rB
# 9O2HV4EkSxJKSZnaj7UlWlmPF0BX5uboEpWmf3CvkbJ+gX9efy17JPEvR8xiqRwI
# 3uGDv3PcoQ043TrlUQJAJtCVSEIdCJdyayRRh+UQasQIddUMTHmW2xPpJHwaMsDs
# jC1HSDwFpetvv+kLBzFTTt76CnJRnxfVbryGE4zSOQ==
# -----END RSA PRIVATE KEY-----
# """
#
# public_key = """
# -----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC85duhn+XToVi4LxZ2Ii+ux1yw
# bpOLZsw/6i2TvUGnaQStBohHewTprh7lZj9ij980aS8ARh25pWeYTWpWg49oMtHG
# hIzFV2uws8fDtc5Hsfg12IO2gXBxWFPvFxCmJghl1iaEn9/We+uGtHgbs3NKj7KN
# I3hL+pOL6OAFEesBdQIDAQAB
# -----END PUBLIC KEY-----
# """
#
#
# # 解密
# def decrypt(text):
#     # RSA对密码进行解密，返回解密后的明文密码
#     random_generator = Random.new().read
#     RSA.generate(1024, random_generator)
#     # with open("pri.pem", "rb") as x:
#     #     e = x.read()
#     rsakey = RSA.importKey(private_key)
#     cipher = PKCS1_v1_5.new(rsakey)
#     decrypted = cipher.decrypt(base64.b64decode(text), random_generator)
#     return decrypted.decode('utf8')
#
#
# # from Cryptodome.PublicKey import RSA
# # from Cryptodome.Cipher import PKCS1_OAEP
#
#
# def generate_key():
#     key = RSA.generate(1024)
#     private_key = key.export_key()
#     print(private_key)
#     with open('private.pem', 'wb') as f:
#         f.write(private_key)
#
#     public_key = key.publickey().export_key()
#     print(public_key)
#     with open('public_key.pem', 'wb') as f:
#         f.write(public_key)
#
# # 实例化生成密钥对文件
# # generate_key()
#
# # 加密
# def encrypt(data):
#     # 导入公钥
#     public_key = RSA.import_key(open('public_key.pem').read())
#     # 加密对象
#     cipher =  PKCS1_OAEP.new(public_key)
#     # 加密
#     msg = cipher.encrypt(data)
#     return msg
#
#
# # 解密
# def decrypt(data):
#     # 导入私钥
#     private_key = RSA.import_key(open('private.pem').read())
#     cipher = PKCS1_OAEP.new(private_key)
#     res = cipher.decrypt(data)
#     return res


def get_first_letter_pinyin(chinese_str):
    result = pinyin(chinese_str, style=Style.FIRST_LETTER)

    #  摊平数组
    def for_for(a):
        return [item for sublist in a for item in sublist]

    result = for_for(result)
    return "".join(result)
