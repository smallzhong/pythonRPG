from monster import Monster
import random
import json
import os
import sys
from monster import Monster


class Battle(object):
    def __init__(self, monster, fighter):
        self._monster = monster
        self._fighter = fighter

    @property
    def monster(self):
        return self._monster

    @property
    def fighter(self):
        return self._fighter

    def fighterNormalAttackMonster(self):
        pass  # 武将普攻怪物

    def monsterNormalAttackFigher(self):
        pass  # 怪物普攻武将

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
