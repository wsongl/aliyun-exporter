#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkdds.request.v20151201.DescribeDBInstancesRequest import DescribeDBInstancesRequest


def mongo_info(credential, region) -> list:
    instances = []
    page_size = 50  # 每页记录数，取值：30、50、100，默认值为30

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeDBInstancesRequest()
    request.set_accept_format('json')
    request.set_PageNumber(1)  # 查询页数，1起始第一页
    request.set_PageSize(page_size)
    response = json.loads(client.do_action_with_exception(request))
    instances = response["DBInstances"]["DBInstance"]

    total_count = response["TotalCount"]
    if total_count > page_size:  # 总的实例数量大于每页显示的实例数量
        pages = total_count // page_size if total_count % page_size == 0 else total_count // page_size + 1
        for page in range(2, pages + 1):
            request.set_PageNumber(page)
            response = json.loads(client.do_action_with_exception(request))
            instances += response["DBInstances"]["DBInstance"]

    return instances
