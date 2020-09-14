# coding:utf-8
# 用来定义全局变量

def init():
    global _global_dict
    _global_dict = {}


def get_value(key, defaultvalue=None):
    return _global_dict.get(key, defaultvalue)


def set_value(key, value):
    _global_dict[key] = value
