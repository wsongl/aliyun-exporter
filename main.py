#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import argparse
import yaml

from web import create_app
from alicloud.alicloud import AliCloud
from collector.collector import AliCloudCollector

from wsgiref.simple_server import make_server
from prometheus_client import REGISTRY


def main():
    # set log
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # parse parm
    parser = argparse.ArgumentParser(description='aliyun exporter args')
    parser.add_argument("-c", "--config", default="default.yml", help="config file of aliyun exporter")
    parser.add_argument('-p', '--port', default=8080, help='port of aliyun exporter service')
    args = parser.parse_args()

    # read config file, generate client of alicloud
    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    alicloudClient = AliCloud(**config)

    # collector
    collector = AliCloudCollector(alicloudClient)
    REGISTRY.register(collector)

    # web
    logging.info('start running aliyun exporter service.')
    app = create_app()
    httpd = make_server('', int(args.port), app)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
