import random 
import logging

from utils import print_message
from action import Action

class Monster(object):

    def __init__(self, name, health, strength, dex):
        self.name = name
        self.health = health
        self.strength = strength
        self.dex = dex
        self.block = 0
        self.weak = 0
        self.vunerable = 0
        self.frail = 0
        self.moveQueue = []
        self.turns = 0

    def getAction(self):
        pass

    def takeDamage(self, damage, hits=1):
        if self.vunerable > 0:
            damage = damage * 1.5

        for x in range(0, hits):
            if damage > self.block:
                adjusted_damage = damage - self.block
                self.block = 0
            else:
                self.block = self.block - damage
                adjusted_damage = 0
            logging.debug("{} takes {} damage".format(self.name, adjusted_damage))
            self.health -= damage

    def isAlive(self):
        return self.health > 0

    def makeWeak(self, weak):
        self.weak = weak
    
    def makeVunerable(self, vunerable):
        self.vunerable = vunerable

    def makeFrail(self, frail):
        self.frail = frail

    def addBlock(self, block):
        if self.frail > 0:
            block = block * 0.5
        self.block = block + self.dex

    def addStrength(self, strength):
        self.strength += strength

    def __str__(self):
        return "{} - {} HP".format(self.name, self.health)

    def startTurn(self):
        self.block = 0

    def endTurn(self):
        self.weak = 0 if self.weak <= 0 else self.weak-1
        self.vunerable = 0 if self.vunerable <= 0 else self.vunerable-1
        self.frail = 0 if self.frail <= 0 else self.frail-1

    def getDamage(self, baseDamage):
        damage = baseDamage + self.strength
        if self.weak > 0:
            damage = damage * 0.75
        return round(damage)

class FatGremlin(Monster):

    def getAction(self):
        return Action(damage=self.getDamage(4), weak=1)


class MadGremlin(Monster):

    def getAction(self):
        return Action(damage=self.getDamage(4))

    def takeDamage(self, damage, hits):
        super(MadGremlin, self).takeDamage(damage, hits)
        self.addStrength(1)


class GremlinWizard(Monster):

    def getAction(self):
        self.turns += 1
        if self.turns < 3:
            return Action()
        elif self.turns == 3: 
            self.turns = 0
            return Action(damage=self.getDamage(25))

class BlueSlaver(Monster):

    def updateQueue(self, action):
        if len(self.moveQueue) == 2:
            self.moveQueue[0] = self.moveQueue[1]
            self.moveQueue[1] = action
        else:
            self.moveQueue.append(action)

    def getAction(self):
        actions = {
        "rake": Action(damage=self.getDamage(7), weak=1),
        "stab": Action(damage=self.getDamage(12))
        }
        if len(self.moveQueue) < 2 or self.moveQueue[0] != self.moveQueue[1]:
            chance = random.randint(0, 100)
            if chance < 40:
                self.updateQueue("rake")
                return actions['rake']
            else:
                self.updateQueue('stab')
                return actions['stab']
        else:
            return actions['rake'] if self.moveQueue[0] != "rake" else actions['stab']

class RedSlaver(Monster):

    def updateQueue(self, action):
        if len(self.moveQueue) == 2:
            self.moveQueue[0] = self.moveQueue[1]
            self.moveQueue[1] = action
        else:
            self.moveQueue.append(action)

    def getAction(self):
        actions = {
        "scrape": Action(damage=self.getDamage(8), vunerable=2),
        "stab": Action(damage=self.getDamage(13))
        }
        self.turns += 1
        if self.turns == 1:
            self.updateQueue('stab')
            return actions['stab']
        else:
            if len(self.moveQueue) < 2 or self.moveQueue[0] != self.moveQueue[1]:
                chance = random.randint(0, 100)
                if chance < 55:
                    self.updateQueue("scrape")
                    return actions['scrape']
                else:
                    self.updateQueue('stab')
                    return actions['stab']
            else:
                return actions['stab'] if self.moveQueue[0] != "stab" else actions['scrape']


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
            'thrash': Action(damage=7, block=5),
            'chomp': Action(damage=12)
        }
        self.turns += 1
        if self.turns == 1:
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
