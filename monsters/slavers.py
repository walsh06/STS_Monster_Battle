import random

from monster import Monster
from action import Action

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
        "scrape": Action(damage=self.getDamage(8), vulnerable=2),
        "stab": Action(damage=self.getDamage(13))
        }
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