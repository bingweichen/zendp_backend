#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : service.py
@Time    : 2021/4/17 5:09 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
from common import errors

client = AcsClient('XXX', 'XXX', 'XXX')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https')  # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('SignName', "XXX")
request.add_query_param('TemplateCode', "XXX")


class Service:
    @staticmethod
    def send_captcha_by_sms(phone_number, captcha):
        request.add_query_param('PhoneNumbers', phone_number)
        
        template_param = {
            'code': captcha
        }
        
        request.add_query_param('TemplateParam', json.dumps(template_param))
        response = client.do_action_with_exception(request)
        convert_response = str(response, encoding='utf-8')
        if json.loads(convert_response)['Code'] != 'OK':
            raise errors.SendSmsFailedException(convert_response)
        return convert_response


if __name__ == '__main__':
    # Service.send_captcha_by_sms(xxx, 121231)
    pass
