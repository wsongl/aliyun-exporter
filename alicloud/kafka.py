#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def kafka_info(credential, region) -> list:
    instances =[]

    client = AcsClient(region_id=region, credential=credential)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('alikafka.{}.aliyuncs.com'.format(region))
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2019-09-16')
    request.set_action_name('GetInstanceList')
    request.add_query_param('RegionId', region)

    response = json.loads(client.do_action(request))
    instances = response["InstanceList"]["InstanceVO"]
    
    return instances
