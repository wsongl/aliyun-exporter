#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
from aliyunsdkvpc.request.v20160428.DescribeNatGatewaysRequest import DescribeNatGatewaysRequest
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.acs_exception.exceptions import ClientException
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest


def nat_gateway_info(credential, region) -> list:
    # https://next.api.aliyun.com/api/Vpc/2016-04-28/DescribeNatGateways?sdkStyle=old&params={}&tab=DEMO&lang=PYTHON
    instances = []

    client = AcsClient(region_id=region, credential=credential)
    request = DescribeNatGatewaysRequest()
    request.set_accept_format('json')
    response = json.loads(client.do_action_with_exception(request))
    instances = response["NatGateways"]["NatGateway"]

    return instances
