#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest


def clb_info(credential, region) -> list:
    instances = []

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeLoadBalancersRequest()
    request.set_accept_format('json')
    response = json.loads(client.do_action_with_exception(request))
    instances = response["LoadBalancers"]["LoadBalancer"]
    
    return instances
