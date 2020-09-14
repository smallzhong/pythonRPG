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


class Fighter(object):
    def __init__(self, **kwargs):
        self._hp = kwargs['hp']
        self._attackdict = kwargs['skill']
        self._equip = kwargs['equip']
        # self._level = kwargs['level']

    @property
    def hp(self):
        return self._hp

    @property
    def equip(self):
        return self._equip

    @property
    def attackdict(self):
        return self._attackdict

    # 减HP
    def minushp(self, h):
        self._hp -= h

    # 加HP
    def addhp(self, h):
        self._hp += h

    # 物理攻击
    def normalattack(self):
        # 随机选择一种物理攻击
        key = random.choice(list(self._attackdict.keys()))
        attackpoint = random.uniform(self._attackdict[key][0], self._attackdict[key][1] + 1)
        return key, attackpoint  # 返回攻击名称和攻击点数
