#!/usr/bin/python
# -*- coding: utf-8 -*-


def _init():                 # 初始化,定义一个全局变量
    global _global_dict
    _global_dict = {}


def set_value(key, value):    # 设置值
    _global_dict[key] = value


def get_value(key, defValue=None):  # 获取值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue