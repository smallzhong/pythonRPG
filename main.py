# coding:utf-8
import random
import time
import json
import pickle
from my_exceptions import BreakPointException, BreakPointException2
from monster import Monster
import os
from fighter import Fighter
from battle import Battle
import sys

g_filepath = ''
g_userdata = {}
g_username = ''
g_mon = [
    {
        '朱蛤': {"name": "朱蛤", "qi": 50, "level": 0, "hp": 105, "skill": {'毒雨': [70, 95]}, "cost": {'毒雨': 30}}
    },
    {
        '野猴': {"name": "野猴", "qi": 50, "level": 1, "hp": 300, "skill": {'灵猴探宝': [150, 200]}, "cost": {'灵猴探宝': 30}},
        '赤蜘蛛': {"name": "赤蜘蛛", "qi": 70, "level": 1, "hp": 400, "skill": {'毒焰': [250, 400]}, "cost": {'毒焰': 60}}
    },
    {
        '花斑虎': {"name": "花斑虎", "qi": 70, "level": 2, "hp": 500, "skill": {'虎啸山林': [350, 450]}, "cost": {'虎啸山林': 70}}
    },
    {
        '腐尸道人': {'name': '腐尸道人', 'qi': 100, 'level': 3, 'hp': 700, 'skill': {'锁灵环': [500, 600]}, 'cost': {'锁灵环': 80}}
    },
    {
        '黑蝎王': {'name': '黑蝎王', 'qi': 120, 'level': 4, 'hp': 1000, 'skill': {"毒沼": [700, 800]}, 'cost': {"毒沼": 100}}
    }
]
g_equip = [
    {'name': '锋灵刃', "price": 500, "hurt": [60, 90]},
    {'name': '玄瞑剑', 'price': 1200, 'hurt': [120, 150]},
    {'name': '碎痕', 'price': 2100, 'hurt': [200, 240]},
    {'name': '慑天', 'price': 3500, 'hurt': [460, 500]},
    {'name': '玉柄龙吟剑', 'price': 4300, 'hurt': [600, 700]}
]


def get_in_store():
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    global g_equip
    print(f'{g_username}，欢迎来到商店！您当前共有{g_userdata["money"]}金币。', end='')
    try:
        while 1:
            t = input('1.查看并购买商品，2.购买八公山豆腐(回精回气)，3.卖出物品，4.离开商店')
            if t == '1':
                try:
                    while 1:
                        equipct = len(g_equip)
                        print(f'\t当前商店共有{equipct}件商品')
                        ct = 0
                        for i in g_equip:
                            print(f'\t{ct}.武器名：{i["name"]}，价格：{i["price"]}金币，伤害加成：{i["hurt"][0]}~{i["hurt"][1]}')
                            ct += 1
                        # 判断用户是否有足够的金钱来购买武器
                        if g_userdata['money'] < g_equip[0]['price']:
                            print(f'您当前只有{g_userdata["money"]}金币，无法购买任何武器，去打怪赚些金币再来吧~')
                            raise BreakPointException
                        t1 = input('如需购买武器请输入武器的编号，需退出请输入任意非数字字符:')
                        try:
                            t1 = int(t1)
                        except ValueError:
                            break
                        if t1 < 0 or t1 >= equipct:
                            print('编号输入错误！没有这件武器！')
                            continue
                        else:
                            if g_userdata['money'] < g_equip[t1]['price']:
                                print(f'您当前拥有的金币数为{g_userdata["money"]}，不足以购买{g_equip[t1]["name"]}！')
                                continue
                            else:
                                g_userdata['money'] -= g_equip[t1]['price']
                                g_userdata['backpack'].append(g_equip[t1])
                                print(
                                    f'购买{g_equip[t1]["name"]}成功！'
                                    f'花费{g_equip[t1]["price"]}金币。您当前剩余{g_userdata["money"]}金币')
                                raise BreakPointException
                except BreakPointException:
                    pass
            elif t == '2':
                try:
                    while 1:
                        t2 = input(f'购买八公山豆腐将消耗200金币，恢复200精和100气，'
                                   f'您当前金币数为{g_userdata["money"]}，是否确认购买？1.确认购买，2.放弃购买')
                        if t2 == '1':
                            if g_userdata['money'] >= 200:
                                g_userdata['money'] -= 200
                                # TODO：到时候要可以选择喂给哪个武将
                                g_userdata['hero']['云天河']['hp'] += 200
                                g_userdata['hero']['云天河']['qi'] += 100
                                print(f"购买成功，当前云天河精为{g_userdata['hero']['云天河']['hp']}，"
                                      f"气为{g_userdata['hero']['云天河']['qi']}，"
                                      f"剩余金钱为{g_userdata['money']}")
                                raise BreakPointException
                            else:
                                print('您没有足够的金币！')
                                raise BreakPointException
                        elif t2 == '2':
                            raise BreakPointException
                        else:
                            continue
                except BreakPointException:
                    pass
            elif t == '3':
                try:
                    while 1:
                        t2 = input('请输入您想要进行的操作，1.查看并卖出商品。2.返回商店主菜单')
                        if t2 == '1':
                            t_ct = 0
                            # 如果背包里面没有东西
                            if not g_userdata['backpack']:
                                print('背包里面什么能卖的东西都没有哦，下次再来吧~')
                                raise BreakPointException  # 退出卖东西菜单

                            for i in g_userdata['backpack']:
                                print(f'\t{t_ct}.{i["name"]}，伤害{i["hurt"][0]}~{i["hurt"][1]}，'
                                      f'回收价格：{i["price"] // 2}')
                                t_ct += 1
                            try:
                                while 1:
                                    try:
                                        while 1:
                                            t3 = input('请输入您想要卖出的物品的编号，如需退出请输入任意非数字字符')
                                            t3 = int(t3)
                                            break
                                    except ValueError:
                                        break
                                        continue
                                    if t3 < 0 or t3 >= len(g_userdata['backpack']):
                                        print('您的背包中没有这个编号的物品！')
                                        continue
                                    else:
                                        g_userdata['money'] += g_userdata['backpack'][t3]['price'] // 2  # 加金钱
                                        print(f"您已成功卖出{g_userdata['backpack'][t3]['name']}，"
                                              f"获得{g_userdata['backpack'][t3]['price'] // 2}金币，"
                                              f"当前金币数量为{g_userdata['money']}。"
                                              f"欢迎下次再来~")
                                        g_userdata['backpack'].remove(i)  # 从背包中移除物品
                                        raise BreakPointException
                            except BreakPointException:
                                pass
                        elif t2 == '2':
                            raise BreakPointException
                        else:
                            continue
                except BreakPointException:
                    pass
            elif t == '4':
                raise BreakPointException
            else:
                continue
    except BreakPointException:
        return


# 根据当前等级 **随机** 挑选怪物
def get_monster():
    global g_mon  # 获取全局变量
    global g_userdata

    d = g_mon[g_userdata['level']]
    t_key = random.choice(list(d.keys()))
    value = d.get(t_key)
    return t_key, value


def my_print_info():
    global g_filepath
    global g_userdata
    global g_username
    global g_mon
    for key in g_userdata['hero']:
        print(f'\t{g_userdata["hero"][key]["name"]}当前状态：精：{g_userdata["hero"][key]["hp"]}，'
              f'气：{g_userdata["hero"][key]["qi"]}，等级：{g_userdata["hero"][key]["level"]}，'
              f'经验值：{g_userdata["hero"][key]["exp"]}。', end='')
    print(f'当前拥有{g_userdata["money"]}金币')


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
        g_userdata['money'] += g_userdata['level'] * 500  # 升到1级增加500金币，2级增加1000，以此类推
        # print('\t您升了%d级！当前级数为%d，金钱数为%d' % (levels_up, g_userdata['level'], g_userdata['money']))

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
    print('欢迎来到仙剑的世界。')
    while 1:
        t = input('请输入1.读取存档，2.新建存档')
        if t == '1':
            name = input('请输入您要读取的存档中玩家的姓名')
            t_filepath = name + '.txt'  # TODO:这里可以更改保存的路径
            g_filepath = t_filepath
            g_username = name
            if read_file(t_filepath):
                break
            else:
                continue

        elif t == '2':
            name = input('请输入您的昵称')
            t_filepath = name + '.txt'
            if os.path.exists(t_filepath):
                print('此昵称已被注册！')
                continue
            else:
                g_userdata = {'money': 1000,
                              'exp': 0,  # 这里加上一个总体的经验吧，可以用来设定不同难度的怪物
                              'level': 0,  # 总体的等级
                              'backpack': [],  # 背包，初始时背包为空
                              'hero': {
                                  '云天河':
                                      {
                                          "name": "云天河",
                                          "exp": 0,
                                          "hp": 130,
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
        t = input('1.开始打怪，2查看背包，3查看或修改武将装备，4进入商店，5查看武将状态，6存档，7读档，8退出游戏')
        if t == '1':
            mon = get_monster()
            # print(mon)
            print('当前有如下武将:', end='')
            for key in g_userdata['hero'].keys():
                print(key)
            a = input('请输入您想要派出的武将，1.云天河')
            if a != '1':
                continue
            else:
                a = '云天河'
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
                    f'\t战斗进行中，{a}剩余{battle.fighter.hp if battle.fighter.hp > 0 else 0}精，剩余{battle.fighter.qi}气，'
                    f'{mon[0]}剩余{battle.monster.hp if battle.monster.hp > 0 else 0}精，剩余{battle.monster.qi}气')

            # 战斗结束后获取战斗结果，进行加气、判断升级等操作
            res = battle.res()
            # 如果不是通过逃跑结束的战斗，则正常结算
            if not res['isflee']:
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
                        res['fighterhp'] + (g_userdata['level'] + 1) * 20  # 加精(level + 1) * 20
                    check_updgrade()  # 判断是否升级
            # 如果是通过逃跑结束的战斗，则不给予胜利奖励
            else:
                g_userdata['hero'][res['name']]['qi'] = res['fighterqi']  # 设定武将的气，没有胜利的奖励
                g_userdata['hero'][res['name']]['hp'] = res['fighterhp']  # 设定武将的精，没有胜利的奖励
                print(f"您成功通过逃跑的方式结束战斗，当前精剩余{g_userdata['hero'][res['name']]['hp']}，"
                      f"气剩余{g_userdata['hero'][res['name']]['qi']}。"
                      f"下次打怪的时候要权衡实力呢，如果觉得打不过可以到商店买八公山豆腐补充精和气哦~")
            del battle  # 删除战斗类，释放内存空间
        # 商店
        elif t == '2':
            if not g_userdata['backpack']:
                print('背包中没有任何物品！去商店看看吧~')
                continue
            else:
                print(f'\t当前背包内共有{len(g_userdata["backpack"])}件物品')
                ct = 0  # 下标从0开始吧，后面更换装备的时候也是
                for i in g_userdata['backpack']:
                    print(f'\t{ct}.{i["name"]}，出售价格{i["price"] // 2}，伤害区间{i["hurt"][0]}~{i["hurt"][1]}')
                    ct += 1

        elif t == '3':
            try:
                while 1:
                    t1 = input('1.查看所有武将的装备，2.更换云天河的装备，3.退出..(其他武将待添加)')
                    if t1 == '1':
                        for i in g_userdata['hero'].values():
                            print(
                                f'角色：{i["name"]}，装备：{list(i["equip"].keys())[0]}，'
                                f'伤害加成：{i["equip"][list(i["equip"].keys())[0]][0]}~'
                                f'{i["equip"][list(i["equip"].keys())[0]][1]}')
                    elif t1 == '2':
                        print(f'\t当前背包内共有{len(g_userdata["backpack"])}件物品')
                        ct = 0
                        for i in g_userdata['backpack']:
                            print(f'\t{ct}.{i["name"]}，出售价格{i["price"] // 2}，伤害区间{i["hurt"][0]}~{i["hurt"][1]}')
                            ct += 1
                        try:
                            while 1:
                                t2 = input('请输入您要装备的装备编号，输入任意非数字字符退出:')
                                #  防止输入的不是一个数字
                                try:
                                    t2 = int(t2)
                                    raise BreakPointException
                                except ValueError:
                                    raise BreakPointException2
                        except BreakPointException:
                            pass
                        except BreakPointException2:
                            raise BreakPointException
                        # 防止输入数字错误
                        if t2 < 0 or t2 >= len(g_userdata['backpack']):
                            print('输入错误！没有这件武器！')
                            continue
                        else:
                            g_userdata['hero']['云天河']['equip'] = {
                                g_userdata['backpack'][t2]['name']: g_userdata['backpack'][t2]['hurt']}
                            print(f"更换装备成功！云天河的装备已被成功换成{g_userdata['backpack'][t2]['name']}！")
                    elif t1 == '3':
                        raise BreakPointException
                    else:
                        continue
            except BreakPointException:
                pass

        elif t == '4':
            get_in_store()

        elif t == '5':
            my_print_info()

        elif t == '6':
            save_file()
            print(f'存档成功！')

        elif t == '7':
            read_file(g_filepath)
            my_print_info()

        elif t == '8':
            sys.exit(0)
        else:
            pass
