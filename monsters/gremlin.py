import random 

from monster import Monster
from action import Action


class GremlinNob(Monster):

    def getAction(self):
        actions = {
            "skull bash": Action(damage=self.getDamage(6), vulnerable=2),
            "rush": Action(damage=self.getDamage(14))
        }
        if self.turns == 1:
            return Action()
        elif self.checkMoveQueueThree("rush"):
            action = "skull bash"
        else:
            chance = random.randint(0, 100)
            if chance < 33:
                action = "skull bash"
            else:
                action = "rush"
        self.updateQueue(action)
        return actions[action]


class GremlinLeader(Monster):

    def getAction(self):
        actions = {
            "stab": Action(damage=self.getDamage(6), hits=3)
            "encourage": Action(strength=3, block=6)
        }
        if self.turns == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                action = "stab"
            else:
                action = "encourage"
        elif self.moveQueue[0] == "stab":
            action = "encourage"
        else:
            action = "stab"
        self.updateQueue(action)
        return actions[action]

    
class FatGremlin(Monster):

    def getAction(self):
        return Action(damage=self.getDamage(4), weak=1)


class MadGremlin(Monster):

    def getAction(self):
        return Action(damage=self.getDamage(4))

    def takeDamage(self, damage, hits, attacker=None):
        super(MadGremlin, self).takeDamage(damage, hits, attacker)
        self.addStrength(1)


class GremlinWizard(Monster):

    def getAction(self):
        if self.turns < 3:
            return Action()
        elif self.turns == 3: 
            self.turns = 0
            return Action(damage=self.getDamage(25))


class ShieldGremlin(Monster):
    
    def getAction(self):
        return Action(damage=self.getDamage(6))


class SneakyGremlin(Monster):

    def getAction(self):
        return Action(damage=self.getDamage(9))
