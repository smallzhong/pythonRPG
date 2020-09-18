#coding:utf-8
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
        self._qi = kwargs['qi']
        self._name = kwargs['name']
        self._cost = kwargs['cost']
        self._level = kwargs['level']
        self._exp = kwargs['exp']

    @property
    def exp(self):
        return self._exp

    @property
    def level(self):
        return self._level

    @property
    def cost(self):
        return self._cost

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
    def equip(self):
        return self._equip

    @property
    def attackdict(self):
        return self._attackdict

    # 获取角色装备的加成
    def getequipaddition(self):
        for value in self.equip.values():
            pass  # 获取当前装备的伤害
        # 装备加成的范围内随机返回一值
        return int(random.uniform(value[0], value[1] + 1))

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
    def normalattack(self):
        # 随机选择一种物理攻击
        key = random.choice(list(self._attackdict.keys()))
        attackpoint = random.uniform(self._attackdict[key][0], self._attackdict[key][1] + 1)
        return key, attackpoint  # 返回攻击名称和攻击点数
