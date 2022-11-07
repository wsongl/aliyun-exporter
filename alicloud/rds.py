#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest


def rds_info(credential, region) -> list:
    instances = []
    page_size = 50  # 每页记录数，取值：1~100，默认为30

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeDBInstancesRequest()
    request.set_accept_format('json')
    request.set_PageSize(page_size)
    response = json.loads(client.do_action_with_exception(request))
    instances = response["Items"]["DBInstance"]

    while True:
        if response["NextToken"] != "":
            request.set_NextToken(response["NextToken"])
            response = json.loads(client.do_action_with_exception(request))
            instances += response["Items"]["DBInstance"]
        else:
            break

    return instances
