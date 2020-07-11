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


class Lagavulin(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Lagavulin, self).__init__(name, health, strength, dex)
        self.asleep = True
        self.stunned = False
        self.attack_count = 0
        self.block = 8

    def getAction(self):
        actions = {
            "siphon": Action(remove_dex=1, remove_strength=1),
            "attack": Action(damage=18),
            "sleep": Action(block=8),
            "stunned": Action()
        }

        if self.asleep and self.turns <= 3:
            action = "sleep"
        elif self.stunned:
            action = "stunned"
            self.stunned = False
        elif self.attack_count < 2:
            action = "attack"
            self.asleep = False
            self.attack_count += 1
        else:
            action = "siphon"
            self.attack_count = 0

        return actions[action]

    def takeDamage(self, damage, hits=1, attacker=None):
        super(Lagavulin, self).takeDamage(damage, hits, attacker)
        if self.asleep and self.block <= 0:
            self.stunned = True
            self.asleep = False


class Nemesis(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Nemesis, self).__init__(name, health, strength, dex)
        self.burn_count = 0

    def getAction(self):
        actions = {
            "debuff": Action(),
            "attack": Action(damage=6, hits=3),
            "scythe": Action(damage=45)
        }

        if self.turns == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                action = "debuff"
            else:
                action = "attack"
        else:
            attack_chance = 35
            debuff_chance = 70
            chance = random.randint(0, 100)

            if self.checkMoveQueueThree("attack"):
                attack_chance = -1
                debuff_chance = 53
            elif self.checkMoveQueueTwo("debuff"):
                attack_chance = 53
                debuff_chance = -1
            elif self.checkMoveQueueTwo("scythe"):
                attack_chance = 50
                debuff_chance = 100

            if chance < attack_chance:
                action = "attack"
            elif chance < debuff_chance:
                action = "debuff"
            else:
                action = "scythe"
        
        if action == "debuff":
            self.burn_count += 2

        chance = random.randint(0, 100)
        if chance < ((self.burn_count/(self.burn_count + 30)) * 5):
            actions[action].damage += 2
        
        self.updateQueue(action)
        return actions[action]

    def takeDamage(self, damage, hits=1, attacker=None):
        if self.turns % 2 == 1:
            damage = 1
        super(Nemesis, self).takeDamage(damage, hits, attacker)


class Sentry(Monster):

    def getAction(self):
        if self.turns % 2 == 0:
            return Action(damage=9)
        else:
            return Action()


class SpireShield(Monster):

    def getAction(self):
        actions = {
            "bash": Action(damage=12, remove_strength=1),
            "fortify": Action(block=30),
            "smash": Action(damage=34, block=34)
        }

        if self.turns < 1 and self.turns % 3 == 0:
            action = "smash"
        elif self.checkMoveQueueTwo("fortify"):
            action = "bash"
        elif self.checkMoveQueueTwo("bash"):
            action = "fortify"
        else:
            chance = random.randint(0, 100)
            action = "bash" if chance < 50 else "fortify"
        
        self.updateQueue(action)
        return actions[action]


class SpireSpear(Monster):
    
    def __init__(self, name, health, strength=0, dex=0):
        super(SpireSpear, self).__init__(name, health, strength, dex)
        self.burn_count = 0

    def getAction(self):
        actions = {
            "burn": Action(damage=self.getDamage(5), hits=2),
            "piercer": Action(strength=2),
            "skewer": Action(damage=self.getDamage(10), hits=3)
        }

        if self.turns == 1:
            action = "burn"
        elif self.turns % 3 == 1:
            action = "skewer"
        elif self.checkMoveQueueTwo("piercer"):
            action = "burn"
        elif self.checkMoveQueueTwo("burn"):
            action = "piercer"
        else:
            chance = random.randint(0, 100)
            action = "burn" if chance < 50 else "piercer"
        
        if action == "debuff":
            self.burn_count += 2

        chance = random.randint(0, 100)
        if chance < ((self.burn_count/(self.burn_count + 30)) * 5):
            actions[action].damage += 2
        
        self.updateQueue(action)
        return actions[action]

class Dagger(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Dagger, self).__init__(name, health, strength, dex)

    def getAction(self):
        if self.turns == 1:
            return Action(damage=9)
        elif self.turns == 2:
            self.health = 0
            return Action(damage=25)


class Reptomancer(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Reptomancer, self).__init__(name, health, strength, dex)
        self.daggers = [Dagger("Dagger", 20), Dagger("Dagger", 20)]

    def getAction(self):
        actions = {
            "snake strike": Action(damage=13, hits=2, weak=1),
            "big bite": Action(damage=30),
            "spawn": Action()
        }
        all_actions = []
        if self.turns == 1:
            action = "spawn"
        else:
            snake_strike_chance = 33
            big_bite_chance = 66
            
            if self.checkMoveQueueTwo("snake strike"):
                snake_strike_chance = -1
                big_bite_chance = 50
            elif self.checkMoveQueueTwo("big bite"):
                snake_strike_chance = 50
                big_bite_chance = -1
            elif self.checkMoveQueueThree("spawn"):
                snake_strike_chance = 50
                big_bite_chance = 100

            chance = random.randint(0, 100)
            if chance < snake_strike_chance:
                action = "snake strike"
            elif chance < big_bite_chance:
                action = "big bite"
            else:
                action = "spawn"

        all_actions.append(actions[action])
        for dagger in self.daggers:
            all_actions.append(dagger.getAction())

        if action == "spawn":
            self.daggers.append(Dagger("Dagger", 20))
        
        self.updateQueue(action)
        return all_actions  

    def startTurn(self):
        for dagger in self.daggers:
            dagger.startTurn()
        super(Reptomancer, self).startTurn()

    def endTurn(self):
        for dagger in self.daggers:
            dagger.endTurn()
        
        self.daggers = [dagger for dagger in self.daggers if dagger.health > 0]
        super(Reptomancer, self).endTurn()

