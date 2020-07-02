from monster import Monster
from action import Action

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
