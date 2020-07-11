import random

from monster import Monster
from action import Action

class BookOfStabbing(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(BookOfStabbing, self).__init__(name, health, strength, dex)
        self.attack_one_count = 0

    def getAction(self):
        actions = {
            "attack_one": Action(damage=6, hits=(2+self.attack_one_count)),
            "attack_two": Action(damage=21)
        }

        if self.checkMoveQueueThree("attack_one"):
            action = "attack_two"
        elif self.checkMoveQueueThree("attack_two"):
            action = "attack_one"
        else:
            chance = random.randint(0, 100)
            if chance < 15:
                action = "attack_two"
            else:
                action = "attack_one"

        if action == "attack_one":
            self.attack_one_count += 1

        self.updateQueue(action)
        return actions[action]

class GiantHead(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(GiantHead, self).__init__(name, health, strength, dex)
        self.its_time_count = 0

    def getAction(self):
        actions = {
            "count": Action(damage=13),
            "its time": Action(damage=30+(self.its_time_count * 5)),
            "glare": Action(weak=1)
        }
        if self.turns < 5:
            chance = random.randint(0, 100)
            if self.checkMoveQueueThree("count"):
                action = "glare"
            elif self.checkMoveQueueThree("glare"):
                action = "count"
            else:
                if chance < 50:
                    action = "glare"
                else:
                    action = "count"
        else:
            self.its_time_count += 1
            action = "its time"

        self.updateQueue(action)
        return actions[action]
