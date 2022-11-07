#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import copy
import logging

from .clb import clb_info
from .ecs import ecs_info
from .eip import eip_info
from .elasticsearch import elasticsearch_info
from .kafka import kafka_info
from .mongo import mongo_info
from .oss import oss_info
from .rds import rds_info
from .redis import redis_info
from .dts_migrate import dts_migrate_info
from .dts_sync import dts_sync_info
from .rocketmq import rocketmq_info
from .nat_gateway import nat_gateway_info

from aliyunsdkcore.auth.credentials import AccessKeyCredential


class AliCloud(object):
    def __init__(self, ak="", sk="", regions=[], services=[], metrics={}, project="ops", period=60, statistic="Average", endpoint="metrics.aliyuncs.com") -> None:
        # ak sk：用于登陆阿里云
        # regions：阿里云地域，类型为列表，默认为空。
        # servies：产品服务名，类型为列表，默认为空。
        # metrics：指标类型，类型为字典，默认为空。
        # project：项目名称，所有metric前会加上这个字符串，默认为"ops"，主要是为了当公司有好多套相同代码环境，便于区分。
        # period：指标取值的最近周期时间，默认为60s。
        # statistic：统计方式，默认为"Average"，阿里云上有的种类如下：Average、Minimum、Maximum、Sum、Value。如果某个指标，想用多个统计方式值，就写多个相同metrics名 但不同statistic的指标，readme会详细讲解。
        # endpoint：接入地址，指云监控数据调用的入口地址，如在新加坡，就用新加坡的接入地址。https://help.aliyun.com/document_detail/28616.html
        if ak == "" or sk == "":
            raise ValueError("ak sk不能为空")
        if regions == []:
            raise ValueError("regions不能为空")
        if services == None:
            raise KeyError("当配置文件中包含services字段配置时, 子项一定要有值; 如果不需要该字段, 此字段不用写.")
        if metrics == None:
            raise KeyError("当配置文件中包含metrics字段配置时, 子项一定要有值; 如果不需要该字段, 此字段不用写.")

        self.ak = ak
        self.sk = sk
        self.project = project
        self.period = period
        self.statistic = statistic
        self.endpoint = endpoint
        self.regions = regions
        self.services = []
        self.metrics = {}

        # 给所有services补全regions的参数
        for service in services:
            if "name" not in service:
                raise KeyError("services中的配置项一定要包含key为 name 的项.")

            regionsDeepcopy = copy.deepcopy(regions)
            # 如果有特殊区域配置
            if "regions" in service:
                inner_regions = service["regions"]
                
                for region in inner_regions:
                    # 增加区域
                    if region[-1] == "+":
                        if region[:-1] in regionsDeepcopy:
                            logging.warning("增加的区域{region}已经在{regions}中存在.")
                        else:
                            regionsDeepcopy.append(region[:-1])
                    # 删减区域
                    elif region[-1] == "-":
                        if region[:-1] in regionsDeepcopy:
                            regionsDeepcopy.remove(region[:-1])
                        else:
                            logging.warning(f"删减的区域{region}没有在{regions}中匹配到.")
                    else:
                        raise ValueError("services内region的配置, 最后一个字符只能是 + 或者 - , 表示增加或减少.")
                service["regions"] = regionsDeepcopy
            else:
                service["regions"] = regions

            self.services.append(service)
        
        logging.info(f'services的详细配置信息为: {self.services}')

        # 给所有metrics补全period、statistic的参数
        for namespace, metricsOfNamespace in metrics.items():
            metricsAfterFormat = []
            for metric in metricsOfNamespace:
                if "name" not in metric:
                    raise KeyError("metric指标配置项一定要包含key为 name 的项.")
                if "period" not in metric:
                    metric["period"] = period
                if "statistic" not in metric:
                    metric["statistic"] = statistic

                metricsAfterFormat.append(metric)

            self.metrics[namespace] = metricsAfterFormat

        logging.info(f'metrics的详细配置信息为: {self.metrics}')

    def generate_credential(self) -> AccessKeyCredential:
        return AccessKeyCredential(self.ak, self.sk)

    def get_service_instances(self, region: str, serviceName: str) -> list:
        """
        # 根据服务名、地域，获取到该服务的所有实例详情
        """
        credential = self.generate_credential()

        if serviceName == "clb":
            return clb_info(credential, region)
        elif serviceName == "ecs":
            return ecs_info(credential, region)
        elif serviceName == "eip":
            return eip_info(credential, region)
        elif serviceName == "elasticsearch":
            return elasticsearch_info(credential, region)
        elif serviceName == "kafka":
            return kafka_info(credential, region)
        elif serviceName == "mongo":
            return mongo_info(credential, region)
        elif serviceName == "oss":
            return oss_info(self.ak, self.sk, region)
        elif serviceName == "rds":
            return rds_info(credential, region)
        elif serviceName == "redis":
            return redis_info(credential, region)
        elif serviceName == "dts_migrate":
            return dts_migrate_info(credential, region)
        elif serviceName == "dts_sync":
            return dts_sync_info(credential, region)
        elif serviceName == "rocketmq":
            return rocketmq_info(credential, region)
        elif serviceName == "nat_gateway":
            return nat_gateway_info(credential, region)
        else:
            raise NameError("services中填入错误的服务名, 或者该服务采集实例信息功能未实现.")
