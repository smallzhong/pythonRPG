#coding:utf-8
'战斗类，用来进行战斗和返回战斗的结果'
from monster import Monster
import random
import json
import os
import sys
from monster import Monster
from my_exceptions import BreakPointException
import time


class Battle(object):
    def __init__(self, monster, fighter, turn='f'):
        self._monster = monster
        self._fighter = fighter
        self.__turn = turn  # 用来确定当前是谁的回合，默认武将先行
        self._isflee = False  # 用来确定这场战斗中武将是否为逃跑

    @property
    def isflee(self):
        return self._isflee

    @isflee.setter
    def isflee(self, v):
        self._isflee = v

    @property
    def monster(self):
        return self._monster

    @property
    def fighter(self):
        return self._fighter

    # 武将用技能攻击怪物
    def fighterSkillAttackMonster(self):
        try:
            while 1:
                # print(f'getequipaddition(){self.fighter.getequipaddition()}')
                # 如果正确就raise一个BreakPointException退出循环
                # 用来实现类似GOTO的功能
                print(f'当前是{self.fighter.name}的回合，请选择出招：')
                t_ct = 0  # 用来记录当前招数的编号
                for i in self.fighter.attackdict.items():  # 获取武将的所有招数
                    print(f'{t_ct}.{i[0]}:需要{self.fighter.cost[i[0]]}气')
                    t_ct += 1
                try:
                    while 1:
                        c = input('请输入您想要出的招数的编号')
                        try:
                            c = int(c)  # 判断这个能不能转换为int，如果能则继续
                        except ValueError:
                            print('您的输入不是一个数字！请重新输入！')
                            continue
                        t_ct = 0
                        for i in self.fighter.attackdict.items():
                            if t_ct == c:
                                c = i[0]
                                break
                            else:
                                t_ct += 1
                        if c not in self.fighter.cost:
                            print('此技能不存在！请重新输入！')
                        else:
                            raise BreakPointException  # 输入没有问题则跳出
                except BreakPointException:
                    pass

                # 如果不够气，继续选择
                if self.fighter.cost[c] > self.fighter.qi:
                    print(f'气不足，{self.fighter.name}剩余{self.fighter.qi}气，不足以发动{c}技能！')
                    continue
                else:
                    raise BreakPointException
        except BreakPointException:
            pass

        self.fighter.minusqi(self.fighter.cost[c])  # 减气

        equipaddition = self.fighter.getequipaddition()
        basehurt = int(random.uniform(self.fighter.attackdict[c][0], self.fighter.attackdict[c][1]))
        totalhurt = equipaddition + basehurt
        self.monster.minushp(totalhurt)
        print(f'云天河发动{c}技能对{self.monster.name}造成{totalhurt}点伤害')
        # self.monster.minushp(self.fighter.attackdict[c])

    def monsterSkillAttackFighter(self):
        name, totalhurt = self.monster.skillattack()
        time.sleep(1)
        print(f'\t{self.monster.name}对{self.fighter.name}发动{name}技能造成了{totalhurt}点伤害')
        self.fighter.minushp(totalhurt)  # 武将减精
        for i in self.monster.cost.values():
            self.monster.minusqi(i)  # 怪物减气

    # 武将普攻怪物
    def fighterNormalAttackMonster(self):
        equitAddition = self.fighter.getequipaddition()
        baseHurt = self.fighter.level * 50 + 50  # 基本伤害 = (等级 + 1) * 50
        totalHurt = equitAddition + baseHurt
        self.monster.minushp(totalHurt)  # 怪物减血
        time.sleep(1)  # 攻击的时候停顿一下，增加游戏体验
        print(f'\t{self.fighter.name}对{self.monster.name}发动普通攻击造成了{totalHurt}点伤害')

    # 怪物普攻武将
    def monsterNormalAttackFigher(self):
        totalHurt = (self.monster.level + 1) * 50 + int(
            random.uniform(-45, 45)) * (self.monster.level + 1)  # (level + 1) * 50 + rand(-20, 20) * (level + 1)
        self.fighter.minushp(totalHurt)
        time.sleep(1)
        print(f'\t{self.monster.name}对{self.fighter.name}发动普通攻击造成了{totalHurt}点伤害')

    # 用来选择出招
    def move(self):
        # 武将回合
        if self.__turn == 'f':
            if self.isdone():
                return False
            time.sleep(1)
            t = input('武将回合，请输入选择，1普通攻击，2技能攻击（消耗气），3技能补血（消耗气），4逃跑（一定概率失败），输入其他进行查看双方状态')

            if t == '1':
                print(f'{self.fighter.name}进行普通攻击')
                self.fighterNormalAttackMonster()
                self.__turn = 'm'
                return True

            elif t == '2':
                self.fighterSkillAttackMonster()
                self.__turn = 'm'
                return True

            elif t == '3':
                totalUp = (self.fighter.level + 1) * 50 + int(
                    random.uniform(-10, 100)) * (self.fighter.level + 1)
                # TODO:加入多个武将之后这里的技能要进行修改
                self.fighter.addhp(totalUp)
                qicost = (self.fighter.level + 1) * 25
                self.fighter.minusqi(qicost)  # 减气
                print(f'{self.fighter.name}发动了五气连波技能，消耗{qicost}气，增加了{totalUp}精，当前精为{self.fighter.hp}')
                self.__turn = 'm'
                return True

            elif t == '4':
                t = int(random.uniform(0, self.fighter.level + 2))  # 级数越高逃跑失败概率越小
                if t:
                    print('逃跑成功!')
                    self.isflee = True  # 设定是逃跑的
                    return False  # 返回战斗结束
                else:
                    print('逃跑失败！')
                    self.__turn = 'm'
                    return True

            else:
                return True  # 如果输入错误也返回True，重新进行回合

        elif self.__turn == 'm':
            if self.isdone():
                return False
            c = int(random.uniform(0, 2))  # 如果是0则发动普通攻击，如果是1则发动技能攻击
            # 判断怪物有没有足够的气，如果没有则将c设置为0，即只能发出普通攻击
            for i in self.monster.cost.values():
                if self.monster.qi < i:  # 没有足够的气，则将c设置为0，只能发出普通攻击
                    c = 0
            if c:
                time.sleep(1)
                print(f'怪物回合，{self.monster.name}进行技能攻击')
                self.monsterSkillAttackFighter()
                self.__turn = 'f'  # 到武将的回合
                return True
            else:
                time.sleep(1)
                print(f'怪物回合，{self.monster.name}进行普通攻击')
                self.monsterNormalAttackFigher()
                self.__turn = 'f'  # 到武将的回合
                return True
        else:
            raise ValueError('self.__turn设置错误！')

    # 判断战斗是否结束，如果任一方的HP小于0，说明战斗结束
    def isdone(self):
        if self._monster.hp <= 0:
            return True
        elif self._fighter.hp <= 0:
            return True
        else:
            return False

    # 返回战斗结果
    def res(self):
        # 如果不是逃跑，正常返回
        if not self.isflee:
            if self.monster.hp <= 0:
                winner = 'fighter'
                name = self.fighter.name
            elif self.fighter.hp <= 0:
                winner = 'monster'
                name = self.monster.name
            else:
                raise ValueError('战斗未结束即返回，出现错误！')

            fighterhp = self.fighter.hp
            fighterqi = self.fighter.qi
            return {
                "isflee": False,  # 判断是否为逃跑的字段，打赢后离开为False
                "winner": winner,  # 胜利者是武将还是怪物
                "name": name,
                "fighterhp": fighterhp,  # 结束后武将剩余的精
                "fighterqi": fighterqi  # 结束后武将剩余的气
            }

        else:
            fighterhp = self.fighter.hp
            fighterqi = self.fighter.qi
            name = self.fighter.name  # 如果成功逃跑，则一定没有被打死，不用判断HP是否为0
            return {
                "isflee": True,  # 如果是逃跑的，将isflee字段设置为True
                "name": name,
                "fighterhp": fighterhp,  # 结束后武将剩余的精
                "fighterqi": fighterqi  # 结束后武将剩余的气
            }
