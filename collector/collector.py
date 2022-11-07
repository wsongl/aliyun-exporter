#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib
import asyncio
import logging
import time

from alicloud.alicloud import AliCloud
from alicloud.cms import cms_info
from utils.format_data import get_point_keys, get_point_values

from prometheus_client.core import GaugeMetricFamily


class AliCloudCollector(object):
    def __init__(self, client: AliCloud) -> None:
        self.client = client

    def collect(self) -> GaugeMetricFamily:
        # 项目名  服务s  指标s
        project = self.client.project
        services = self.client.services
        metrics = self.client.metrics

        # 实例(services)数据exporter
        for service in services:
            instances = []

            regions = service["regions"]
            for region in regions:
                instances += self.client.get_service_instances(region, service["name"])

            if len(instances) > 0:
                metric_name = f'{project}_aliyun_{service["name"]}_instance_info'

                keys = get_point_keys(instances[0])
                gauge_info = GaugeMetricFamily(name=metric_name, documentation="", labels=keys)
                for instance in instances:
                    gauge_info.add_metric(labels=get_point_values(instance, keys), value=1)

                yield gauge_info
            else:
                logging.warning(f'服务({service})实例个数为0')

        # 监控指标(metrics)数据exporter
        # tip: 对一个namespace下的metrics，进行了异步获取。对所有namespace而言，则是同步
        for namespace, metricsOfNamespace in metrics.items():
            tasks = []
            loop = asyncio.get_event_loop()

            # 异步获取监控数据
            for index, metric in enumerate(metricsOfNamespace):
                if (index + 1) % 20 == 0:
                    time.sleep(1)  # 阿里云，每秒调用接口的频率限制为，每秒不超过20次
                task = loop.create_task(cms_info(self.client.ak, self.client.sk, self.client.endpoint, namespace, metric))
                tasks.append(task)
            # 等待任务全部完成
            for task in tasks:
                loop.run_until_complete(task)
            # 循环获取每个metric监控数据(metric)
            for index, metric in enumerate(metricsOfNamespace):
                datapoints = tasks[index].result()

                ## 生成指标metric
                if len(datapoints) > 0:
                    metric_name = f'{project}_aliyun_{namespace}_{metric["name"].replace(".", "_")}_{metric["statistic"]}_metric'  # 阿里云指标有存在.这个特殊字符，prometheus不支持，需要替换为_
                    keys = get_point_keys(datapoints[0])
                    gauge_metric = GaugeMetricFamily(name=metric_name, documentation="", labels=keys)
                    for data in datapoints:
                        gauge_metric.add_metric(labels=get_point_values(data, keys), value=data[metric["statistic"]])
                    yield gauge_metric
                else:
                    logging.warning(f'指标({metric})监控项条数为0')
