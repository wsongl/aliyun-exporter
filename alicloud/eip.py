#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkvpc.request.v20160428.DescribeEipAddressesRequest import DescribeEipAddressesRequest


def eip_info(credential, region) -> list:
    instances = []
    page_size = 100  # 查询页面显示的实例数量，最大100

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeEipAddressesRequest()
    request.set_accept_format('json')
    request.set_PageNumber(1)
    request.set_PageSize(page_size)

    response = json.loads(client.do_action_with_exception(request))
    instances = response["EipAddresses"]["EipAddress"]

    total_count = response["TotalCount"]
    if total_count > page_size:  # 总的实例数量大于每页显示的实例数量
        pages = total_count // page_size if total_count % page_size == 0 else total_count // page_size + 1
        for page in range(2, pages + 1):
            request.set_PageNumber(page)
            response = json.loads(client.do_action_with_exception(request))
            instances += response["EipAddresses"]["EipAddress"]

    return instances
