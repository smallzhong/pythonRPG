from monster import Monster
import random
import json
import os
import sys
from monster import Monster
from my_exceptions import BreakPointException

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
        pass

    # 怪物普攻武将
    def monsterNormalAttackFigher(self):
        pass

    # 用来选择出招
    def move(self):
        # 武将回合
        if self.__turn == 'f':
            try:
                while 1:
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

            self.monsterSkillAttackFighter()


        elif self.__turn == 'm':
            print(f'当前是{self.monster.name}的回合，请选择出招：')
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
