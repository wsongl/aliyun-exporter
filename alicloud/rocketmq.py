#!/usr/bin/env python
#coding=utf-8
import json


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def rocketmq_info(credential, region) -> list:
    # 【特殊】公网地域id： mq-internet-access
    client = AcsClient(region_id=region, credential=credential)

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain(f'ons.{region}.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('http')  # https | http
    request.set_version('2019-02-14')
    request.set_action_name('OnsInstanceInServiceList')
    response = json.loads(client.do_action(request))
    instances = response["Data"]["InstanceVO"]

    return instances
