
# aliyun-exporter

[toc]

# 一、介绍

采集阿里云云产品监控指标数据，生成`prometheus exporter`格式内容。
阿里云指标项：https://help.aliyun.com/document_detail/163515.html



# 二、安装

开发环境：python3.8

```bash
pip3 install -r requirements.txt

1. 直接使用：python main.py -p 8080 -c default.yml

2. 打包文件：
   pyinstaller -F main.py -n aliyun-exporter

   ./aliyun-exporter -p 8080 -c default.yml

3. 容器化：  
   docker build -t ops/aliyun-exporter .
   docker run -d --name aliyun-exporter -p 8080:8080 ops/aliyun-exporter
```

Tip：

> -p 为端口参数，默认端口为8080；
> -c 为配置文件参数，默认配置文件为同级目录下default.yml文件；
> 启动时不加参数，则使用默认配置。



# 三、访问
http://IP:Port/metrics

http://localhost:8080/metrics （默认）



# 四、配置文件说明
1. ak、sk：阿里云登录调用api用；
2. project：项目名，会在所有指标名前加上该字段；
3. period：采集周期，从当前时间往前推period长时间；
4. statistic：指标（metric）的统计维度，阿里云常用的有Average、Minimum、Maximum、Sum、Value；
5. endpoint：
6. regions：地域，类型列表；
7. services：服务名，类型列表；
8. metrics：服务指标，类型字典；

Tip：

> services和metrics两者没有依赖关系，获取service信息，为了`grafana`展示的时候，能显示实例名，而不是指标（metric）的实例id。



# 五、扩展新指标

## 5.1、service层

alicloud目录下，添加xx.py，实现获取新服务实例的功能；

alicloud/alicloud.py get_service_instances方法中添加新服务的调用；



## 5.2、metrics层

配置文件中直接添加新监控项即可；




# 六、BUG

## 6.1、dts采集服务实例，返回结果存在重复

【bug描述】
配置了services: dts相关的服务实例时，如果填了多个区域，而某个区域没有dts相关服务实例，则该区域的dts实例会返回其他某个区域的dts实例（如采集了杭州和深圳两个地域，杭州有dts服务实例，深圳没有dts服务实例，则杭州区域返回杭州的dts实例，深圳则会返回杭州的dts实例），导致最终返回的实例有重合；该bug已经和阿里云确认，在老sdk中，的确存在这个bug，并且没有计划修复。

【解决方法】
在services中配置准确的regions范围即可。



# 七、优化

现在公司阿里云的数据采集（不包括ecs），基本能在20s完成一次数据的采集，已经满足需求。



当前瓶颈：

1、阿里云获取ecs实例信息，一次只能获取100台实例数据，如果有2000台ecs，则需要0.8s * 20的时间。

2、services 和 metrics两个指标是串行。

3、阿里云api调用频率限制，为20次/s。



优化点：

解析`yaml`文件时，把所有的services metrics解析成一条一条的记录，保存所有基础信息，再异步方式获取数据。去掉瓶颈2。



