import json
import pickle
import logging
import time
import random

'''
hp:血量
attackDict:攻击技能和相应的伤害,攻击时随机挑选技能
    {'撞击':[300, 500]} 表示撞击这个技能可能的伤害为300~500 

'''


class Monster(object):
    def __init__(self, **kwargs):
        self._hp = kwargs['hp']
        self._attackdict = kwargs['skill']
        self._qi = kwargs['qi']
        self._name = kwargs['name']
        self._level = kwargs['level']
        self._cost = kwargs['cost']

    @property
    def cost(self):
        return self._cost

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name

    @property
    def qi(self):
        return self._qi

    @property
    def hp(self):
        return self._hp

    @property
    def attackdict(self):
        return self._attackdict

    # 减HP
    def minushp(self, h):
        self._hp -= h

    # 加HP
    def addhp(self, h):
        self._hp += h

    # 减气
    def minusqi(self, h):
        self._qi -= h

    # 加气
    def addqi(self, h):
        self._qi += h

    # 物理攻击
    def skillattack(self):
        # 随机选择一种物理攻击
        key = random.choice(list(self._attackdict.keys()))
        attackpoint = random.uniform(self._attackdict[key][0], self._attackdict[key][1] + 1)
        return key, int(attackpoint)  # 返回攻击名称和攻击点数(int)
