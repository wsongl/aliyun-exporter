#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import oss2


def oss_info(ak, sk, region) -> list:
    instances = []
    auth = oss2.Auth(ak, sk)
    service = oss2.Service(auth, 'https://oss-{}.aliyuncs.com'.format(region))

    for bucket in oss2.BucketIterator(service):
        b = {}
        # bucket信息：SimplifiedBucketInfo，Python38/Lib/site-packages/oss2/models.py
        b["name"] = bucket.name
        b["location"] = bucket.location
        b["creation_date"] = bucket.creation_date
        b["extranet_endpoint"] = bucket.extranet_endpoint
        b["intranet_endpoint"] = bucket.intranet_endpoint
        b["storage_class"] = bucket.storage_class
        
        instances.append(b)

    return instances
