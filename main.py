import random
import time
import json
import pickle
from my_exceptions import BreakPointException
from monster import Monster
import gol
import os
from fighter import Fighter
from battle import Battle
import sys

g_filepath = ''
g_userdata = {}
g_username = ''
g_mon = [
    {
        '朱蛤': {"name": "朱蛤", "qi": 50, "level": 0, "hp": 100, "skill": {'毒雨': [30, 50]}, "cost": {'毒雨': 30}}
    },
    {
        '野猴': {"name": "野猴", "qi": 50, "level": 1, "hp": 300, "skill": {'灵猴探宝': [60, 90]}, "cost": {'灵猴探宝': 30}},
        '赤蜘蛛': {"name": "赤蜘蛛", "qi": 70, "level": 1, "hp": 400, "skill": {'毒焰': [100, 150]}, "cost": {'毒焰': 60}}
    },
    {
        '花斑虎': {"name": "花斑虎", "qi": 70, "level": 2, "hp": 500, "skill": {'虎啸山林': [200, 250]}, "cost": {'虎啸山林': 50}}
    }
]
g_equip = [
    {'name': '锋灵刃', "price": 500, "hurt": [60, 90]},
    {'name': '玄瞑剑', 'price': 1200, 'hurt': [120, 150]},
    {'name': '碎痕', 'price': 2100, 'hurt': [200, 240]}
]


# 根据当前等级 **随机** 挑选怪物
def get_monster():
    global g_mon  # 获取全局变量
    global g_userdata

    d = g_mon[g_userdata['level']]
    t_key = random.choice(list(d.keys()))
    value = d.get(t_key)
    return t_key, value


def print_info():
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    print(f'\t当前整体等级：{g_userdata["level"]}，经验值：{g_userdata["exp"]}，金钱数{g_userdata["money"]}')
    for key in g_userdata['hero']:
        print(f'\t{g_userdata["hero"][key]["name"]}当前状态：精：{g_userdata["hero"][key]["hp"]}，'
              f'气：{g_userdata["hero"][key]["qi"]}，等级：{g_userdata["hero"][key]["level"]}，'
              f'经验值：{g_userdata["hero"][key]["exp"]}')


# 检查是否升级
def check_updgrade():
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    levelUpRequire = 300  # 300经验升一级
    if g_userdata['level'] * levelUpRequire < g_userdata['exp']:
        levels_up = (g_userdata['exp'] - g_userdata['level'] * levelUpRequire) // levelUpRequire + 1
        # 更新信息
        g_userdata['level'] += levels_up
        g_userdata['money'] += g_userdata['level'] * 1000  # 升到1级增加1000金币，2级增加2000，以此类推
        print('\t您升了%d级！当前级数为%d，金钱数为%d' % (levels_up, g_userdata['level'], g_userdata['money']))

    for key in g_userdata['hero'].keys():
        if g_userdata['hero'][key]['level'] * levelUpRequire < g_userdata['hero'][key]['exp']:
            levels_up = (g_userdata['hero'][key]['exp'] - g_userdata['hero'][key][
                'level'] * levelUpRequire) // levelUpRequire + 1
            g_userdata['hero'][key]['level'] += levels_up
            g_userdata['hero'][key]['hp'] += g_userdata['hero'][key]['level'] * 100  # 加level * 100点精
            g_userdata['hero'][key]['qi'] += g_userdata['hero'][key]['level'] * 30  # 加level * 30点气
            print(f'\t{key}升了{levels_up}级，当前级数为{g_userdata["hero"][key]["level"]}')

    # 读档操作


def read_file(t_filepath):
    # TODO:封装读档操作
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    if not os.path.exists(t_filepath):
        print('读取存档失败！查无此存档！')
        return False  # 读取存档失败返回False
    else:
        with open(g_filepath, 'rb') as f:
            g_userdata = json.load(f)
            if not g_userdata or g_filepath == '' or g_username == '':  # 如果全局变量设置失败或者序列化失败
                raise ValueError('读档时出现错误！')
        print(f'欢迎您，{g_username}!')
        return True


# 存档操作
def save_file():
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    with open(g_filepath, 'w') as f:
        json.dump(g_userdata, f)
        # TODO:json.dump会有奇怪的错误
        g_username = name
        if not g_userdata or g_filepath == '' or g_username == '':  # 如果全局变量设置失败或者序列化失败
            raise ValueError('进入游戏时出现错误！')


if __name__ == '__main__':
    gol.init()  # 首先初始化全局变量获取模块
    while 1:
        t = input('输入1读取存档，输入2新建存档:')
        if t == '1':
            name = input('请输入您要读取的存档中玩家的姓名')
            t_filepath = 'f:\\' + name + '.txt'  # TODO:这里可以更改保存的路径
            g_filepath = t_filepath
            g_username = name
            if read_file(t_filepath):
                break
            else:
                continue

        elif t == '2':
            name = input('请输入您的昵称')
            t_filepath = 'f:\\\\' + name + '.txt'
            if os.path.exists(t_filepath):
                print('此昵称已被注册！')
                continue
            else:
                # TODO：不能用字典存数据，那就换成类，查一下json.dump如何保存类数据
                g_userdata = {'money': 1000,
                              'exp': 0,  # 这里加上一个总体的经验吧，可以用来设定不同难度的怪物
                              'level': 0,  # 总体的等级
                              'hero': {
                                  '云天河':
                                      {
                                          "name": "云天河",
                                          "exp": 0,
                                          "hp": 100,
                                          "level": 0,
                                          "equip": {"木剑": [30, 50]},
                                          "skill": {"落星式": [100, 200], "膝裂": [200, 300]},
                                          "cost": {"落星式": 25, "膝裂": 40},
                                          "qi": 100
                                      }
                              }
                              }  # 'exp': 0,'name': name,

                g_filepath = t_filepath
                save_file()
                print(f'欢迎您，{g_username}!')
                break

    # 读取或新建存档成功，进入游戏
    while 1:
        # TODO:要可以读取任意时间的存档
        t = input('输入1开始打怪，输入2查看背包，输入3查看自身装备，输入4进入商店，输入5查看武将状态，输入6存档，输入7读档，输入8退出游戏')
        if t == '1':
            mon = get_monster()
            # print(mon)
            print('当前有如下武将:', end='')
            for key in g_userdata['hero'].keys():
                print(key)
            a = input('请输入您想要派出的武将:')
            if a not in g_userdata['hero']:
                print('武将未找到!')
                continue
            # print(g_userdata['hero'][a])
            fighter = Fighter(**g_userdata['hero'][a])  # 传入字典
            # print(mon[1])
            monster = Monster(**mon[1])
            battle = Battle(monster, fighter)  # 创建战斗对象
            print(f'战斗开始，{a}({g_userdata["hero"][a]["level"]}级)对阵{mon[0]}({mon[1]["level"]}级)！'
                  f'{a}剩余{battle.fighter.hp}精，剩余{battle.fighter.qi}气，'
                  f'{mon[0]}剩余{battle.monster.hp}精，剩余{battle.monster.qi}气')
            # while not battle.done():
            #     battle.move()
            while battle.move():  # 如果返回False表明战斗结束
                time.sleep(1)
                print(
                    f'\t战斗进行中，{a}剩余{battle.fighter.hp}精，剩余{battle.fighter.qi}气，'
                    f'{mon[0]}剩余{battle.monster.hp}精，剩余{battle.monster.qi}气')

            # 战斗结束后获取战斗结果，进行加气、判断升级等操作
            res = battle.res()
            print(f'战斗结束！{res["name"]}胜利！')
            if res['winner'] == 'monster':
                print('您被打败了！即将重新读档！')
                if read_file(g_filepath):  # 重新读档
                    print('重新读档成功。')
                else:
                    raise ValueError('重新读档失败！！可能是由于存档文件被破坏')
            else:
                # 战斗胜利，加精加气加经验
                g_userdata['exp'] += (g_userdata['level'] + 1) * 50  # 加经验(level + 1) * 50
                g_userdata['hero'][res['name']]['exp'] += (g_userdata['level'] + 1) * 50  # 武将加经验(level + 1) * 50
                g_userdata['hero'][res['name']]['qi'] = \
                    res['fighterqi'] + (g_userdata['level'] + 1) * 10  # 加气(level + 1) * 10
                g_userdata['hero'][res['name']]['hp'] = \
                    res['fighterhp'] + (g_userdata['level'] + 1) * 50  # 加精(level + 1) * 50
                check_updgrade()  # 判断是否升级

        # 商店
        elif t == '2':
            pass

        elif t == '3':
            pass

        elif t == '4':
            pass

        elif t == '5':
            print_info()

        elif t == '6':
            save_file()
            print(f'存档成功！')

        elif t == '7':
            read_file(g_filepath)
            print_info()

        elif t == '8':
            sys.exit(0)
        else:
            pass
