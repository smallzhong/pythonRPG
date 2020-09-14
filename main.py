import random
import time
import json
import pickle
from monster import Monster
import gol
import os

# 云天河技能：野球拳
g_filepath = ''
g_userdata = {}
g_username = ''


def init():
    pass


def read_file():
    # 设定全局变量
    # global g_filepath
    # global g_username
    # global g_userdata
    # global g_mon
    with open(gol.get_value(g_filepath), 'rb') as f:
        g_userdata = json.load(f)
        # print('重新读档成功。您当前经验值为%d，等级为%d，血量为%d' % (g_userdata['exp'], g_userdata['level'], g_userdata['hp']))
        if not g_userdata or g_filepath == '' or g_filepath == '':  # 如果全局变量设置失败或者序列化失败
            raise ValueError('读档时出现错误！')


if __name__ == '__main__':
    init()
    gol.init()  # 首先初始化全局变量获取模块
    while 1:
        t = input('输入1读取存档，输入2新建存档:')
        if t == '1':
            name = input('请输入您要读取的存档中玩家的姓名')
            t_filepath = 'f:\\' + name + '.txt'  # TODO:这里可以更改保存的路径
            if not os.path.exists(t_filepath):
                print('读取存档失败！查无此存档！')
                continue
            else:
                g_filepath = t_filepath
                g_username = name
                with open(g_filepath, 'rb') as f:
                    g_userdata = json.load(f)
                    if not g_userdata or g_filepath == '' or g_username == '':  # 如果全局变量设置失败或者序列化失败
                        raise ValueError('读档时出现错误！')
                print(f'欢迎您，{g_username}!')
                break

        elif t == '2':
            name = input('请输入您的昵称')
            t_filepath = 'f:\\\\' + name + '.txt'
            if os.path.exists(t_filepath):
                print('此昵称已被注册！')
                continue
            else:
                # g_userdata = {'name': name, 'exp': 0, 'level': 0, 'hp': 100, 'lastrest': 0}  # lastrest为上次休息的时间
                g_userdata = {'money': 1000,
                              'hero': {'云天河':
                                           {"exp": 0,
                                            "level": 0,
                                            "euqip": {"木剑": [30, 50]},
                                            "skill": {"yeqiuquan": [100, 200]}
                                            }
                                       }
                              }  # 'exp': 0,'name': name,

                g_filepath = t_filepath
                with open(g_filepath, 'w') as f:
                    json.dump(g_userdata, f) # , ensure_ascii=False
                    # TODO:json.dump会有奇怪的错误
                    # a = json.dumps(g_userdata)
                    # print(type(a))
                    # f.write(a)
                g_username = name
                if not g_userdata or g_filepath == '' or g_username == '':  # 如果全局变量设置失败或者序列化失败
                    raise ValueError('进入游戏时出现错误！')
                print(f'欢迎您，{g_username}!')
                break

    # 读取或新建存档成功，进入游戏
