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
        self.weak = 0
        self.vunerable = 0
        self.moveQueue = []
        self.turns = 0

    def getAction(self):
        pass

    def takeDamage(self, damage, hits):
        logging.debug("{} takes {} damage {} time(s)".format(self.name, damage, hits))
        if self.vunerable > 0:
            damage = damage * 1.5
        self.health -= damage * hits

    def isAlive(self):
        return self.health > 0

    def makeWeak(self, weak):
        self.weak = weak
    
    def makeVunerable(self, vunerable):
        self.vunerable = vunerable

    def __str__(self):
        return "{} - {} HP".format(self.name, self.health)

    def endTurn(self):
        self.weak = 0 if self.weak <= 0 else self.weak-1
        self.vunerable = 0 if self.vunerable <= 0 else self.vunerable-1

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
        self.strength += 1


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