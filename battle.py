from monster import Monster
import random
import json
import os
import sys
from monster import Monster
from my_exceptions import BreakPointException
import time


# TODO:怪物出招也是随机选择普通攻击或者技能攻击，如果气没了则只进行技能攻击

class Battle(object):
    def __init__(self, monster, fighter, turn='f'):
        self._monster = monster
        self._fighter = fighter
        self.__turn = turn  # 用来确定当前是谁的回合，默认武将先行

    @property
    def monster(self):
        return self._monster

    @property
    def fighter(self):
        return self._fighter

    # 武将用技能攻击怪物
    def fighterSkillAttackMonster(self):
        pass

    def monsterSkillAttackFighter(self):
        pass

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
        totalHurt = self.monster.level * 50 + 50
        self.fighter.minushp(totalHurt)
        time.sleep(1)
        print(f'\t{self.monster.name}对{self.fighter.name}发动普通攻击造成了{totalHurt}点伤害')

    # 用来选择出招
    def move(self):
        # 武将回合
        if self.__turn == 'f':
            time.sleep(1)
            t = input('武将回合，请输入选择，1普通攻击，2技能攻击（消耗气），3技能补血（消耗气），4逃跑（一定概率失败）')

            if t == '1':
                self.fighterNormalAttackMonster()
                # TODO：攻速？
                self.__turn = 'm'

            elif t == '2':
                try:
                    while 1:
                        print(f'getequipaddition(){self.fighter.getequipaddition()}')
                        # 如果正确就raise一个BreakPointException退出循环
                        # 用来实现类似GOTO的功能
                        print(f'当前是{self.fighter.name}的回合，请选择出招：')
                        for i in self.fighter.attackdict.items():  # 获取武将的所有招数
                            # TODO：这里要让用户可以用数字来选择出招
                            print(f'{i[0]}:需要{self.fighter.cost[i[0]]}气')
                        c = input('请输入您想要出的招数')
                        if c not in self.fighter.cost:
                            print('此技能不存在！请重新输入！')
                        else:
                            raise BreakPointException
                except BreakPointException:
                    pass

                self.fighterSkillAttackMonster()


        elif self.__turn == 'm':
            # TODO:这里要随机挑选技能攻击或者普通攻击
            time.sleep(1)
            print(f'\t怪物回合，{self.monster.name}进行普通攻击')
            self.monsterNormalAttackFigher()
            self.__turn = 'f'  # 到武将的回合3
            # print(f'当前是{self.monster.name}的回合，请选择出招：')
        else:
            raise ValueError('self.__turn设置错误！')

    # 判断战斗是否结束
    def done(self):
        if self._monster.hp == 0:
            return True
        elif self._fighter.hp == 0:
            return True
        else:
            return False

    # 返回战斗结果
    def res(self):
        pass
