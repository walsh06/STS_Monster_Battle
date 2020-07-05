import random

from monster import Monster
from action import Action

class Pointy(Monster):

    def getAction(self):
        return Action(damage=5, hits=2)

class Bear(Monster):

    def getAction(self):
        if self.turns == 1:
            return Action(remove_dex=2)
        elif self.turns % 2 == 0:
            return Action(damage=18)
        else:
            return Action(damage=9, block=9)

class Romeo(Monster):

    def getAction(self):
        if self.turns == 1:
            return Action()
        elif self.turns % 2 == 0:
            return Action(damage=15)
        else:
            return Action(damage=10, weak=2)


class Mugger(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Mugger, self).__init__(name, health, strength, dex)
        self.lunged = False
        self.smoke_bombed = False

    def startTurn(self):
        super(Mugger, self).startTurn()
        if self.smoke_bombed:
            self.health = 0

    def getAction(self):
        if self.turns < 3:
            return Action(damage=10)
        elif self.lunged:
            self.smoke_bombed = True
            return Action(block=11)
        elif self.smoke_bombed:
            return Action()
        else:
            chance = random.randint(0, 100)
            if chance < 50:
                self.lunged = True
                return Action(damage=16)
            else:
                self.smoke_bombed = True
                return Action(block=11)

class Looter(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Looter, self).__init__(name, health, strength, dex)
        self.lunged = False
        self.smoke_bombed = False

    def startTurn(self):
        super(Looter, self).startTurn()
        if self.smoke_bombed:
            self.health = 0
            
    def getAction(self):
        if self.turns < 3:
            return Action(damage=10)
        elif self.lunged:
            self.smoke_bombed = True
            return Action(block=6)
        elif self.smoke_bombed:
            return Action()
        else:
            chance = random.randint(0, 100)
            if chance < 50:
                self.lunged = True
                return Action(damage=12)
            else:
                self.smoke_bombed = True
                return Action(block=6)