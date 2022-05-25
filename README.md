# aliyun-exporter

### 介绍

采集阿里云云产品监控指标数据，生成 prometheus exporter 格式内容。
阿里云指标项：https://help.aliyun.com/document_detail/163515.html

### 安装

python 环境：python3.8
pip3 install -r requirements.txt

1. 直接使用：python main.py -p 8080 -c default.yml
2. 打包文件：
   pyinstaller -F main.py -n aliyun-exporter-v1.0.0
   ./aliyun-exporter-v1.0.0 -p 8080 -c default.yml
3. 容器化：  
   docker build -t ops/aliyun-exporter:v1.0.0 .
   docker run -d --name aliyun-exporter -p 8080:8080 ops/aliyun-exporter:v1.0.0

**tip:**
-p 为端口参数，默认端口为 8080；
-c 为配置文件参数，默认配置文件为同级目录下 default.yml 文件；
启动时如果不加参数，则使用默认配置。

### 访问

http://IP:Port/metrics
http://localhost:8080/metrics （默认）

### 配置文件说明

- ak、sk：阿里云AccessKey；
- project：项目名，会在所有指标名前加上该字段，默认"ops"。主要为了同一公司内，有多套相同代码环境，用该字段来区分；
- period：采集周期，单位秒，默认60，表示采集时间范围为 当前时间到往前推 period 时间；
- statistic：指标（metric）的统计维度，阿里云常用的有 Average、Minimum、Maximum、Sum、Value，默认"Average"；
- endpoint：接入地址，日志监控(cms)服务查询监控数据时，访问的接入地址；服务部署在哪，就用该地区的接入地址。默认采用中国国内统一接入地址(metrics.aliyuncs.com)。
- regions：全局地域，类型列表，表示服务实例采集的地域；
- services：服务名，类型字典；
  
  
  
  完整的服务（service）字段如下：

```yml
- name: service_name  # 服务名
  regions:            # 特殊地域，与全局地域共同组成一个服务的地域范围
    - region_1+       # 增加的地域（结尾为+）
    - region_2-       # 删除的地域（结尾为-）
```

特殊地域与全局地域的使用说明，如果全局地域配置为["region1", "region2", "region3"]，特殊地域配置为["region4+", "region1-"]，则该服务最后的地域配置为["region2", "region3","region4"]。



- metrics：服务指标，类型字典；
  
  完整的指标（metric）字段如下：

```yml
namespace_name:        # 命名空间
  - name: metric_name  # 指标名称
    period: 60         # 采集周期，可选，该位置的值会覆盖全局位置的值
    statistic: statistic_type # 统计维度，可选，该位置的值会覆盖全局位置的值
```



Tip：

services 和 metrics 两者没有依赖关系，

services是获取实例信息；metrics是获取实例的各项指标监控数据。两者结合，才能在 grafana 展示的时候，显示实例名，而不是只有实例id。



### 扩展新服务

1. alicloud 目录下，添加 xx.py，实现获取新服务实例的功能；
2. alicloud/alicloud.py get_service_instances 方法中添加新服务的调用；



### BUG

1. dts 采集服务实例，返回结果存在重复
   【bug 描述】
   配置了 services: dts 相关的服务实例时，如果填了多个区域，而某个区域没有 dts 相关服务实例，则该区域的 dts 实例会返回其他某个区域的 dts 实例（如采集了杭州和深圳两个地域，杭州有 dts 服务实例，深圳没有 dts 服务实例，则杭州区域返回杭州的 dts 实例，深圳则会返回杭州的 dts 实例），导致最终返回的实例有重合；该 bug 已经和阿里云确认，在老 sdk 中，的确存在这个 bug，并且没有计划修复。

【解决方法】
建议在 prometheus 的 promSQL 中来实现去重。
考虑到代码简洁性和避坑方法难易性，故我这边也没有做代码层面去重。
