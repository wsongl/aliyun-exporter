#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def elasticsearch_info(credential, region) -> list:
    instances =[]
    page_size = 50  # 分页查询时设置的每页条数。最大值：100，默认为10

    client = AcsClient(region_id=region, credential=credential)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_method('GET')
    request.set_protocol_type('https')  # https | http
    request.set_domain('elasticsearch.{}.aliyuncs.com'.format(region))
    request.set_version('2017-06-13')
    request.add_query_param('size', page_size)
    request.add_query_param('page', "1")
    request.add_header('Content-Type', 'application/json')
    request.set_uri_pattern('/openapi/instances')

    response = json.loads(client.do_action_with_exception(request))
    instances = response["Result"]

    total_count = response["Headers"]["X-Total-Count"]
    if total_count > page_size:  # 总的实例数量大于每页显示的实例数量
        pages = total_count // page_size if total_count % page_size == 0 else total_count // page_size + 1
        for page in range(2, pages + 1):
            request.set_PageNumber(page)
            response = json.loads(client.do_action_with_exception(request))
            instances += response["Result"]

    return instances
