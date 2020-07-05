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

    def removeDex(self, dex):
        self.dex -= dex

    def __str__(self):
        return "{} - {} HP".format(self.name, self.health)

    def startTurn(self):
        self.block = 0
        self.turns += 1

    def endTurn(self):
        self.weak = 0 if self.weak <= 0 else self.weak-1
        self.vunerable = 0 if self.vunerable <= 0 else self.vunerable-1
        self.frail = 0 if self.frail <= 0 else self.frail-1

    def getDamage(self, baseDamage):
        damage = baseDamage + self.strength
        if self.weak > 0:
            damage = damage * 0.75
        return round(damage)
