#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import json

from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models


async def cms_info(ak, sk, endpoint, namespace, metric) -> list:
    datapoints = []

    config = open_api_models.Config(access_key_id=ak, access_key_secret=sk)
    config.endpoint = endpoint
    client = Cms20190101Client(config)

    describe_metric_last_request = cms_20190101_models.DescribeMetricLastRequest(
        namespace=namespace,
        metric_name=metric["name"],
        period=metric["period"],
    )
    runtime = util_models.RuntimeOptions()
    
    response = await client.describe_metric_last_with_options_async(describe_metric_last_request, runtime)
    datapoints = [] if response.body.datapoints == None else json.loads(response.body.datapoints)
    next_token = response.body.next_token

    # nex_token
    while True:
        if next_token != None and next_token != "":
            describe_metric_last_request = cms_20190101_models.DescribeMetricLastRequest(
                namespace=namespace,
                metric_name=metric["name"],
                period=metric["period"],
                next_token=next_token
            )
            response = await client.describe_metric_last_with_options_async(describe_metric_last_request, runtime)
            datapoints += json.loads(response.body.datapoints)
            next_token = response.body.next_token
        else:
            break

    return datapoints
