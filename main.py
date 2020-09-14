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
g_mon = {'朱蛤': {"hp": 100, "skill": {'毒雨': [30, 50]}},
         '野猴': {"hp": 150, "skill": {'灵猴探宝': [60, 90]}}
         }


def get_monster():
    pass


def check_update():
    pass


if __name__ == '__main__':
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
                g_userdata = {'money': 1000,
                              'hero': {'云天河':
                                           {"exp": 0,
                                            "hp": 100,
                                            "level": 0,
                                            "euqip": {"木剑": [30, 50]},
                                            "skill": {"落星式": [100, 200], "膝裂": [100, 200]}
                                            }
                                       }
                              }  # 'exp': 0,'name': name,

                g_filepath = t_filepath
                with open(g_filepath, 'w') as f:
                    json.dump(g_userdata, f)
                    # TODO:json.dump会有奇怪的错误
                    g_username = name
                    if not g_userdata or g_filepath == '' or g_username == '':  # 如果全局变量设置失败或者序列化失败
                        raise ValueError('进入游戏时出现错误！')
                print(f'欢迎您，{g_username}!')
                break

    # 读取或新建存档成功，进入游戏
    while 1:
        # TODO:要可以读取任意时间的存档
        t = input('输入1开始打怪，输入2查看背包，输入3查看自身装备，输入4查看角色属性，输入5存档，输入6读档，输入7退出游戏')
        if t == '1':
            mon = get_monster()
