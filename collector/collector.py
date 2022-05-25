#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import asyncio
import logging
from prometheus_client.core import GaugeMetricFamily

from alicloud.cms import cms_info
from utils.format_data import get_point_keys, get_point_values
from alicloud.alicloud import AliCloud


class AliCloudCollector(object):
    def __init__(self, client: AliCloud) -> None:
        self.client = client

    def collect(self) -> GaugeMetricFamily:
        # 项目名 区域  服务名  指标
        project = self.client.project
        regions = self.client.regions
        endpoint = self.client.endpoint
        services = self.client.services
        metrics = self.client.metrics

        ### 实例信息
        for service in services:
            instances = []

            regions = service["regions"]
            for region in regions:
                instances += self.client.get_service_instances(region, service["name"])

            ## 生成实例metric
            if len(instances) > 0:
                metric_name = f'{project}_aliyun_info_{service["name"]}'

                keys = get_point_keys(instances[0])
                gauge_info = GaugeMetricFamily(name=metric_name, documentation="", labels=keys)
                for instance in instances:
                    gauge_info.add_metric(labels=get_point_values(instance, keys), value=1)

                yield gauge_info
            else:
                logging.warning(f'服务({service})实例个数为0')

        # ### 监控指标metrics
        for namespace, metricsOfNamespace in metrics.items():
            tasks = []
            loop = asyncio.get_event_loop()

            # 异步获取监控数据
            for _, metric in enumerate(metricsOfNamespace):
                task = loop.create_task(cms_info(self.client.ak, self.client.sk, self.client.endpoint, namespace, metric))
                tasks.append(task)
            for task in tasks:
                loop.run_until_complete(task)

            for i, metric in enumerate(metricsOfNamespace):
                datapoints = tasks[i].result()

                ## 生成指标metric
                if len(datapoints) > 0:
                    metric_name = f'{project}_aliyun_metric_{namespace}_{metric["name"].replace(".", "_")}_{metric["statistic"]}'
                    keys = get_point_keys(datapoints[0])
                    gauge_metric = GaugeMetricFamily(name=metric_name, documentation="", labels=keys)
                    for data in datapoints:
                        gauge_metric.add_metric(labels=get_point_values(data, keys), value=data[metric["statistic"]])
                    yield gauge_metric
                else:
                    logging.warning(f'指标({metric})监控项条数为0')
