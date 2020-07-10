import random 
import logging

from utils import print_message
from action import Action

class Monster(object):

    def __init__(self, name, health, strength=0, dex=0):
        self.name = name
        self.health = health
        self.strength = strength
        self.dex = dex
        self.block = 0
        self.weak = 0
        self.vulnerable = 0
        self.frail = 0
        self.moveQueue = []
        self.turns = 0
        self.thorns = 0
        self.runaway = False
        self.artifact = 0

    def getAction(self):
        pass

    def takeDamage(self, damage, hits=1, attacker=None):
        if self.vulnerable > 0:
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
            
            if self.thorns > 0:
                attacker.health -= self.thorns

    def isAlive(self):
        return self.health > 0

    def ran_away(self):
        return self.runaway

    def makeWeak(self, weak):
        if self.artifact > 0:
            self.weak = weak
        else:
            self.artifact -= 1
    
    def makevulnerable(self, vulnerable):
        if self.artifact <= 0:
            self.vulnerable = vulnerable
        else:
            self.artifact -= 1

    def makeFrail(self, frail):
        if self.artifact <= 0:
            self.frail = frail
        else:
            self.artifact -= 1

    def addBlock(self, block):
        if self.frail <= 0:
            block = block * 0.5
        self.block = block + self.dex

    def addStrength(self, strength):
        self.strength += strength

    def removeDex(self, dex):
        if self.artifact <= 0:
            self.dex -= dex
        else:
            self.artifact -= 1
    def __str__(self):
        return "{} - {} HP".format(self.name, self.health)

    def startTurn(self):
        self.block = 0
        self.turns += 1

    def endTurn(self):
        self.weak = 0 if self.weak <= 0 else self.weak-1
        self.vulnerable = 0 if self.vulnerable <= 0 else self.vulnerable-1
        self.frail = 0 if self.frail <= 0 else self.frail-1

    def getDamage(self, baseDamage):
        damage = baseDamage + self.strength
        if self.weak > 0:
            damage = damage * 0.75
        return round(damage)

    def updateQueue(self, action, limit=2):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > limit:
            self.moveQueue.pop(limit)

    def checkMoveQueueTwo(self, move):
        return len(self.moveQueue) > 0 and self.moveQueue[0] == move

    def checkMoveQueueThree(self, move):
        return len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == move
