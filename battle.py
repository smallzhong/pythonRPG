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

    def res(self):
        pass  # 战斗结果
