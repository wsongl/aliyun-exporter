#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


def ecs_info(credential, region) -> list:
    instances = []

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_PageSize(100)  # 每次请求，返回实例数量

    response = json.loads(client.do_action_with_exception(request))
    instances = response["Instances"]["Instance"]

    while True:  
        if response["NextToken"] != "":
            request.set_NextToken(response["NextToken"])
            response = json.loads(client.do_action_with_exception(request))
            instances += response["Instances"]["Instance"]
        else:
            break
    
    return instances
