import random

from monster import Monster
from action import Action

class Cultist(Monster):

    def getAction(self):
        if self.turns == 1:
            return Action()
        else:
            return Action(damage=self.getDamage(6))
    
    def endTurn(self):
        super(Cultist, self).endTurn()
        if self.turns > 1:
            self.strength += 3


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

    def __init__(self, name, health, strength=0, dex=0):
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
        if len(self.moveQueue) > 0 and self.moveQueue[0] == 'grow':
            self.updateQueue('bite')
            return actions['bite']
        elif len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == 'bite':
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
        
class RedLouse(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(RedLouse, self).__init__(name, health, strength, dex)
        self.curl = False

    def updateQueue(self, action):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > 2:
            self.moveQueue.pop(2)

    def getAction(self):
        actions = {
            'grow': Action(strength=3),
            'bite': Action(damage=self.getDamage(6))
        }
        if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1]:
            if self.moveQueue[0] == 'grow':
                self.updateQueue('bite')
                return actions['bite']
            else:
                self.updateQueue('grow')
                return actions['grow']
        else:
            chance = random.randint(0, 100)
            if chance < 75:
                self.updateQueue('bite')
                return actions['bite']
            else:
                self.updateQueue('grow')
                return actions['grow']
    
    def takeDamage(self, damage, hits=1):
        for hit in range(0, hits):
            super(RedLouse, self).takeDamage(damage, 1)
            if not self.curl:
                self.curl = True
                self.block = 5

class GreenLouse(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(GreenLouse, self).__init__(name, health, strength, dex)
        self.curl = False

    def updateQueue(self, action):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > 2:
            self.moveQueue.pop(2)

    def getAction(self):
        actions = {
            'spit web': Action(weak=2),
            'bite': Action(damage=self.getDamage(6))
        }
        if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1]:
            if self.moveQueue[0] == 'spit web':
                self.updateQueue('bite')
                return actions['bite']
            else:
                self.updateQueue('spit web')
                return actions['spit web']
        else:
            chance = random.randint(0, 100)
            if chance < 75:
                self.updateQueue('bite')
                return actions['bite']
            else:
                self.updateQueue('spit web')
                return actions['spit web']
    
    def takeDamage(self, damage, hits=1):
        for hit in range(0, hits):
            super(GreenLouse, self).takeDamage(damage, 1)
            if not self.curl:
                self.curl = True
                self.block = 5

class Byrd(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Byrd, self).__init__(name, health, strength, dex)
        self.flying = True
        self.stunned = False
        self.knockdown_turns = 0
        
    def updateQueue(self, action):
        self.moveQueue.insert(0, action)
        if len(self.moveQueue) > 1:
            self.moveQueue.pop(1)

    def getAction(self):
        if self.flying:
            actions = {
                "peck": Action(damage=self.getDamage(1), hits=5),
                "swoop": Action(damage=self.getDamage(12)),
                "caw": Action(strength=1),
            }
            chance = random.randint(0, 100)
            peck_chance = 50
            swoop_chance = 70

            if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == "peck":
                peck_chance = -1
                swoop_chance = 45
            elif len(self.moveQueue) > 0 and self.moveQueue[0] == "swoop":
                peck_chance = 60
                swoop_chance = -1
            elif len(self.moveQueue) > 0 and self.moveQueue[0] == "caw":
                peck_chance = 65
                swoop_chance = 100

            if chance < peck_chance:
                self.updateQueue("peck")
                return actions['peck']
            elif chance < swoop_chance:
                self.updateQueue("swoop")
                return actions['swoop']
            else:
                self.updateQueue("caw")
                return actions['caw']
        else:
            actions = {
                "headbutt": Action(damage=self.getDamage(3)),
                "fly": Action(),
            }
            if self.knockdown_turns == 0:
                self.stunned = False
                self.knockdown_turns += 1
                return Action()
            elif self.knockdown_turns == 1:
                self.knockdown_turns += 1
                return actions["headbutt"]
            else:
                self.knockdown_turns = 0
                self.flying = True
                self.moveQueue = []
                return actions['fly']

    def takeDamage(self, damage, hits):
        flying_hits = 0
        for hit in range(0, hits): 
            flying_hits += 1
            if flying_hits < 3:
                super(Byrd, self).takeDamage(damage*0.5, 1)
            else:
                self.stunned = True
                self.flying = False
                super(Byrd, self).takeDamage(damage, 1)

