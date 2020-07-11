import random

from monster import Monster
from action import Action


class SuperSlime(Monster):

    def __init__(self, split_class, split_name, name, health, strength=0, dex=0):
        super(SuperSlime, self).__init__(name, health, strength, dex)
        self.slimes = []
        self.split = False
        self.starting_health = health
        self.split_class = split_class
        self.split_name = split_name

    
    def startTurn(self):
        super(SuperSlime, self).startTurn()
        for slime in self.slimes:
            slime.startTurn()

    def endTurn(self):
        super(SuperSlime, self).endTurn()
        for slime in self.slimes:
            slime.endTurn()
        self.slimes = [slime for slime in self.slimes if slime.isAlive()]

    def removeDex(self, dex):
        if self.split:
            self.slimes[0].removeDex(dex)
        else:
            super(SuperSlime, self).removeDex(dex)

    def removeStrength(self, strength):
        if self.split:
            self.slimes[0].removeStrength(strength)
        else:
            super(SuperSlime, self).removeStrength(strength)

    def makeWeak(self, weak):
        if self.split:
            self.slimes[0].makeWeak(weak)
        else:
            super(SuperSlime, self).makeWeak(weak)
    
    def makevulnerable(self, vulnerable):
        if self.split:
            self.slimes[0].makevulnerable(vulnerable)
        else:
            super(SuperSlime, self).makevulnerable(vulnerable)

    def makeFrail(self, frail):
        if self.split:
            self.slimes[0].makeFrail(frail)
        else:
            super(SuperSlime, self).makeFrail(frail)

    def takeDamage(self, damage, hits=1, attacker=None):
        if self.split:
            self.slimes[0].takeDamage(damage, hits, attacker)
        else:
            super(SuperSlime, self).takeDamage(damage, hits, attacker)
            if self.health <= self.starting_health/2 and self.health > 0:
                self.split = True
                self.slimes = (self.split_class(self.split_name, self.health), 
                               self.split_class(self.split_name, self.health))
            
    def isAlive(self):
        if self.split:
            return len(self.slimes) > 0
        else:
            return super(SuperSlime, self).isAlive()


class SmallAcidSlime(Monster):

    def getAction(self):
        actions = {
            "tackle": Action(damage=3),
            "lick": Action(weak=1)
        }
        if self.turns == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                action = "tackle"
            else:
                action = "lick"
        elif self.checkMoveQueueTwo("tackle"):
            action = "lick"
        else:
            action = "tackle"

        self.updateQueue(action)
        return actions[action]


class MediumAcidSlime(SuperSlime):
    
    def __init__(self, name, health, strength=0, dex=0):
        super(MediumAcidSlime, self).__init__(SmallAcidSlime, "Small Acid Slime", name, health, strength, dex)

    def getAction(self):
        actions = {
            "spit": Action(damage=7),
            "lick": Action(weak=1),
            "tackle": Action(damage=10)
        }
        all_actions = []
        if self.split:
            for slime in self.slimes:
                all_actions.append(slime.getAction())
        else:
            spit_chance = 40
            lick_chance = 70

            if self.checkMoveQueueTwo("lick"):
                spit_chance = 55
                lick_chance = -1
            elif self.checkMoveQueueThree("spit"):
                spit_chance = -1
                lick_chance = 50
            elif self.checkMoveQueueThree("tackle"):
                spit_chance = 55
                lick_chance = 100

            chance = random.randint(0, 100)

            if chance < spit_chance:
                action = "spit"
            elif chance < lick_chance:
                action = "lick"
            else:
                action = "tackle"

            all_actions = [actions[action]]
            self.updateQueue(action)
        
        return all_actions


class LargeAcidSlime(SuperSlime):
    
    def __init__(self, name, health, strength=0, dex=0):
        super(LargeAcidSlime, self).__init__(MediumAcidSlime, "Medium Acid Slime", name, health, strength, dex)

    def getAction(self):
        actions = {
            "spit": Action(damage=11),
            "lick": Action(weak=2),
            "tackle": Action(damage=16)
        }
        all_actions = []
        if self.split:
            for slime in self.slimes:
                all_actions.extend(slime.getAction())
        else:
            spit_chance = 40
            lick_chance = 70

            if self.checkMoveQueueTwo("lick"):
                spit_chance = 55
                lick_chance = -1
            elif self.checkMoveQueueThree("spit"):
                spit_chance = -1
                lick_chance = 50
            elif self.checkMoveQueueThree("tackle"):
                spit_chance = 55
                lick_chance = 100

            chance = random.randint(0, 100)

            if chance < spit_chance:
                action = "spit"
            elif chance < lick_chance:
                action = "lick"
            else:
                action = "tackle"

            all_actions = [actions[action]]
            self.updateQueue(action)
        
        return all_actions


class SmallSpikeSlime(Monster):

    def getAction(self):
        return [Action(damage=5)]


class MediumSpikeSlime(SuperSlime):

    def __init__(self, name, health, strength=0, dex=0):
        super(MediumSpikeSlime, self).__init__(SmallSpikeSlime, "Small Spike Slime", name, health, strength, dex)


    def getAction(self):
        actions = {
            "lick": Action(frail=1),
            "tackle": Action(damage=8)
        }
        all_actions = []
        if self.split:
            for slime in self.slimes:
                all_actions.extend(slime.getAction())
        else:
            chance = random.randint(0, 100)

            if self.checkMoveQueueThree("lick"):
                action = "tackle"
            elif self.checkMoveQueueThree("tackle"):
                action = "lick"
            elif chance < 30:
                action = "tackle"
            else:
                action = "lick"
            all_actions = [actions[action]]
            self.updateQueue(action)
        
        return all_actions


class LargeSpikeSlime(SuperSlime):

    def __init__(self, name, health, strength=0, dex=0):
        super(LargeSpikeSlime, self).__init__(MediumSpikeSlime, "Medium Spike Slime", name, health, strength, dex)

    def getAction(self):
        actions = {
            "lick": Action(frail=2),
            "tackle": Action(damage=16)
        }
        all_actions = []
        if self.split:
            for slime in self.slimes:
                all_actions.extend(slime.getAction())
        else:
            chance = random.randint(0, 100)

            if self.checkMoveQueueThree("lick"):
                action = "tackle"
            elif self.checkMoveQueueThree("tackle"):
                action = "lick"
            elif chance < 30:
                action = "tackle"
            else:
                action = "lick"
            all_actions = [actions[action]]
            self.updateQueue(action)
        
        return all_actions