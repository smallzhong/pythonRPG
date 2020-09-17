'战斗类，用来进行战斗和返回战斗的结果'
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
        try:
            while 1:
                # print(f'getequipaddition(){self.fighter.getequipaddition()}')
                # 如果正确就raise一个BreakPointException退出循环
                # 用来实现类似GOTO的功能
                print(f'当前是{self.fighter.name}的回合，请选择出招：')
                t_ct = 0  # 用来记录当前招数的编号
                for i in self.fighter.attackdict.items():  # 获取武将的所有招数
                    # TODO：这里要让用户可以用数字来选择出招
                    print(f'{t_ct}.{i[0]}:需要{self.fighter.cost[i[0]]}气')
                    t_ct += 1
                c = int(input('请输入您想要出的招数的编号'))
                t_ct = 0
                # TODO:这里可能会超限，可以试试BreakPointExcept
                for i in self.fighter.attackdict.items():
                    if t_ct == c:
                        c = i[0]
                        break
                    else:
                        t_ct += 1
                if c not in self.fighter.cost:
                    print('此技能不存在！请重新输入！')
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
                self.fighterNormalAttackMonster()
                # TODO：攻速？
                self.__turn = 'm'
                return True

            elif t == '2':
                self.fighterSkillAttackMonster()
                self.__turn = 'm'
                return True

            elif t == '3':
                # TODO:用气加血
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
                # TODO:增加随机逃跑方法
                print('逃跑失败！')
                self.__turn = 'm'
                return True

            else:
                return True  # 如果输入错误也返回True，重新进行回合

        elif self.__turn == 'm':
            # TODO:这里要随机挑选技能攻击或者普通攻击
            if self.isdone():
                return False
            time.sleep(1)
            print(f'怪物回合，{self.monster.name}进行普通攻击')
            self.monsterNormalAttackFigher()
            self.__turn = 'f'  # 到武将的回合3
            return True
            # print(f'当前是{self.monster.name}的回合，请选择出招：')
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
        # TODO:这里要返回战斗的结果
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
            "winner": winner,  # 胜利者是武将还是怪物
            "name": name,
            "fighterhp": fighterhp,  # 结束后武将剩余的精
            "fighterqi": fighterqi  # 结束后武将剩余的气
        }
