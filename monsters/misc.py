import random

from monster import Monster
from action import Action

class Cultist(Monster):

    def getAction(self):
        self.turns += 1
        if self.turns == 1:
            return Action()
        else:
            return Action(damage=self.getDamage(6))
    
    def endTurn(self):
        super(Cultist, self).endTurn()
        if self.turns > 1:
            self.strength += 3


class Pointy(Monster):

    def getAction(self):
        return Action(damage=5, hits=2)


class Centurion(Monster):

    def getAction(self):
        actions = {
            "fury": Action(damage=self.getDamage(6), hits=3),
            "slash": Action(damage=self.getDamage(12))
        }
        chance = random.randint(0, 100)
        if chance < 65:
            return actions['fury']
        else:
            return actions['slash']


class JawWorm(Monster):

    def __init__(self, name, health, strength, dex):
        super(JawWorm, self).__init__(name, health, strength, dex)
        self.block = 6
        self.strength += 3

    def updateQueue(self, action):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > 3:
            self.moveQueue.pop(3)

    def getAction(self):
        actions = {
            'bellow': Action(block=6, strength=3),
            'thrash': Action(damage=self.getDamage(7), block=5),
            'chomp': Action(damage=self.getDamage(12))
        }
        self.turns += 1
        if self.turns == 1:
            self.updateQueue('chomp')
            return actions['chomp']
        else:
            bellow_chance = 45
            thrash_chance = 30
            if len(self.moveQueue) > 1 and self.moveQueue[0] == 'bellow' and self.moveQueue[0] == self.moveQueue[1]:
                bellow_chance = -1
                thrash_chance = 52
            if len(self.moveQueue) > 2 and self.moveQueue[0] == 'thrash' and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == self.moveQueue[2]:
                bellow_chance = 60
                thrash_chance = -1

            chance = random.randint(0, 100)

            if chance < bellow_chance:
                self.updateQueue('bellow')
                return actions['bellow']
            elif chance < thrash_chance:
                self.updateQueue('thrash')
                return actions['thrash']
            else:
                self.updateQueue('chomp')
                return actions['chomp']

class FungiBeast(Monster):

    def updateQueue(self, action):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > 3:
            self.moveQueue.pop(3)

    def getAction(self):
        actions = {
            'grow': Action(strength=3),
            'bite': Action(damage=self.getDamage(6)),
        }
        if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == 'grow':
            self.updateQueue('bite')
            return actions['bite']
        elif len(self.moveQueue) > 2 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == self.moveQueue[2] and self.moveQueue[0] == 'bite':
            self.updateQueue('grow')
            return actions['grow']
        else:
            chance = random.randint(0, 100)
            if chance < 60:
                self.updateQueue('bite')
                return actions['bite']
            else:
                self.updateQueue('grow')
                return actions['grow']
        
