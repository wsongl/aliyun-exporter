#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib

# 根据一个point（一个实例数据 或 一个监控数据）信息，获取该point的keys值；
# 只取val为int str float类型的key，一方面，复杂的类型不好处理，也没有共性的处理方式；另外，获取了也没什么用；
# Average Minimum Maximum Sum Value 这些去除，是在指标（metric）层的监控数据，不需要当成维度，故而去除；
def get_point_keys(point):
    keys = []

    for key, val in point.items():
        if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
            if key == "Average" or key == "Minimum" or key == "Maximum" or key == "Sum" or key == "Value" or key == "timestamp":
                pass
            else:
                keys.append(str(key))
    return keys

def get_point_values(point, keys):
    """
    根据keys, 返回point对应key的values
    @params: point: 一条记录值
    @params: point中value对应的keys
    @return: 
    """
    vals = []

    for key in keys:
        if key in point:
            vals.append(str(point[key]))
        else:
            vals.append("")  # 当字段没有匹配，则加空字符串，防止key -> val没有一一对应，产生错位

    return vals
