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

    def getAction(self):
        actions = {
            'bellow': Action(block=6, strength=3),
            'thrash': Action(damage=self.getDamage(7), block=5),
            'chomp': Action(damage=self.getDamage(12))
        }
        if self.turns == 1:
            self.updateQueue('chomp', 3)
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
                self.updateQueue('bellow', 3)
                return actions['bellow']
            elif chance < thrash_chance:
                self.updateQueue('thrash', 3)
                return actions['thrash']
            else:
                self.updateQueue('chomp', 3)
                return actions['chomp']

class FungiBeast(Monster):

    def getAction(self):
        actions = {
            'grow': Action(strength=3),
            'bite': Action(damage=self.getDamage(6)),
        }
        if len(self.moveQueue) > 0 and self.moveQueue[0] == 'grow':
            self.updateQueue('bite', 3)
            return actions['bite']
        elif len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1] and self.moveQueue[0] == 'bite':
            self.updateQueue('grow', 3)
            return actions['grow']
        else:
            chance = random.randint(0, 100)
            if chance < 60:
                self.updateQueue('bite', 3)
                return actions['bite']
            else:
                self.updateQueue('grow', 3)
                return actions['grow']
        
class RedLouse(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(RedLouse, self).__init__(name, health, strength, dex)
        self.curl = False

    def getAction(self):
        actions = {
            'grow': Action(strength=3),
            'bite': Action(damage=self.getDamage(6))
        }
        if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1]:
            if self.moveQueue[0] == 'grow':
                self.updateQueue('bite', 2)
                return actions['bite']
            else:
                self.updateQueue('grow', 2)
                return actions['grow']
        else:
            chance = random.randint(0, 100)
            if chance < 75:
                self.updateQueue('bite', 2)
                return actions['bite']
            else:
                self.updateQueue('grow', 2)
                return actions['grow']
    
    def takeDamage(self, damage, hits=1, attacker=None):
        for hit in range(0, hits):
            super(RedLouse, self).takeDamage(damage, 1, attacker)
            if not self.curl:
                self.curl = True
                self.block = 5

class GreenLouse(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(GreenLouse, self).__init__(name, health, strength, dex)
        self.curl = False

    def getAction(self):
        actions = {
            'spit web': Action(weak=2),
            'bite': Action(damage=self.getDamage(6))
        }
        if len(self.moveQueue) > 1 and self.moveQueue[0] == self.moveQueue[1]:
            if self.moveQueue[0] == 'spit web':
                self.updateQueue('bite', 2)
                return actions['bite']
            else:
                self.updateQueue('spit web', 2)
                return actions['spit web']
        else:
            chance = random.randint(0, 100)
            if chance < 75:
                self.updateQueue('bite', 2)
                return actions['bite']
            else:
                self.updateQueue('spit web', 2)
                return actions['spit web']
    
    def takeDamage(self, damage, hits=1, attacker=None):
        for hit in range(0, hits):
            super(GreenLouse, self).takeDamage(damage, 1, attacker)
            if not self.curl:
                self.curl = True
                self.block = 5

class Byrd(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Byrd, self).__init__(name, health, strength, dex)
        self.flying = True
        self.stunned = False
        self.knockdown_turns = 0

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
                self.updateQueue("peck", 1)
                return actions['peck']
            elif chance < swoop_chance:
                self.updateQueue("swoop", 1)
                return actions['swoop']
            else:
                self.updateQueue("caw", 1)
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

    def takeDamage(self, damage, hits, attacker=None):
        flying_hits = 0
        for hit in range(0, hits): 
            flying_hits += 1
            if flying_hits < 3:
                super(Byrd, self).takeDamage(damage*0.5, 1, attacker)
            else:
                self.stunned = True
                self.flying = False
                super(Byrd, self).takeDamage(damage, 1, attacker)


class Chosen(Monster):

    def getAction(self):
        actions = {
            "poke": Action(damage=self.getDamage(5), hits=2),
            "zap": Action(damage=self.getDamage(18)),
            "debilitate": Action(damage=self.getDamage(10), vulnerable=2),
            "drain": Action(weak=3, strength=3),
            "hex": Action()
        }
        if self.turns == 1:
            return actions["poke"]
        elif self.turns ==2:
            return actions["hex"]
        elif self.turns % 2 == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                return actions['debilitate']
            else:
                return actions['drain']
        else:
            chance = random.randint(0, 100)
            if chance < 40:
                return actions['zap']
            else:
                return actions['poke']

class Darkling(Monster):

    def getAction(self):
        actions = {
            "nip": Action(damage=9),
            "chomp": Action(damage=8, hits=2),
            "harden": Action(block=12)
        }
        if self.turns == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                self.updateQueue("nip", 1)
                return actions["nip"]
            else:
                self.updateQueue("harden", 1)
                return actions["harden"]
        else:
            nip_chance = 30
            chomp_chance = 70
            if self.checkMoveQueueThree("nip"):
                nip_chance = -1
                chomp_chance = 55
            elif self.checkMoveQueueTwo("harden"):
                nip_chance = 45
                chomp_chance = 100
            elif self.checkMoveQueueTwo("chomp"):
                nip_chance = 50
                chomp_chance = -1
            
            chance = random.randint(0, 100)

            if chance < nip_chance:
                self.updateQueue("nip", 1)
                return actions["nip"]
            elif chance < chomp_chance:
                self.updateQueue("chomp")
                return actions["chomp"]
            else:
                self.updateQueue("harden")
                return actions["harden"]


class Exploder(Monster):

    def getAction(self):
        if self.turns < 3:
            return Action(damage=9)
        else:
            self.health = 0
            return Action(damage=30)


class TheMaw(Monster):

    def getAction(self):
        actions = {
            "roar": Action(weak=3, frail=3),
            "drool": Action(strength=3),
            "slam": Action(damage=self.getDamage(25)),
            "nom": Action(damage=5, hits=self.turns/2)
        }
        if self.turns == 1:
            self.updateQueue("roar", 1)
            return actions["roar"]
        else:
            chance = random.randint(0, 100)

            if self.moveQueue[0] == "nom":
                self.updateQueue("drool", 1)
                return actions["drool"]
            elif self.moveQueue[0] == "drool" or self.moveQueue[0] == "roar":
                if chance < 50:
                    self.updateQueue("nom", 1)
                    return actions["nom"]
                else:
                    self.updateQueue("slam", 1)
                    return actions["slam"]
            if self.moveQueue[0] == "slam":                
                if chance < 50:
                    self.updateQueue("nom", 1)
                    return actions["nom"]
                else:
                    self.updateQueue("drool", 1)
                    return actions["drool"]

class Mystic(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Mystic, self).__init__(name, health, strength, dex)
        self.starting_health = health

    def getAction(self):
        actions = {
            "heal": Action(),
            "buff": Action(strength=2),
            "attack": Action(damage=self.getDamage(8), frail=2)
        }
        if self.starting_health - self.health >= 16 and not self.checkMoveQueueThree("heal"):
            self.updateQueue("heal", 2)
            self.health += 16
            return actions["heal"]
        else:
            chance = random.randint(0, 100)
            if self.checkMoveQueueThree("buff"):
                action = "attack"
            elif self.checkMoveQueueThree("attack"):
                action = "buff"
            else:
                chance = random.randint(0, 100)
                if chance < 60:
                    action = "attack"
                else:
                    action = "buff"

            self.updateQueue(action)
            return actions[action]

class OrbWalker(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(OrbWalker, self).__init__(name, health, strength, dex)
        self.burn_count = 0

    def getAction(self):
        actions = {
            "laser": Action(damage=self.getDamage(10), strength=3),
            "claw": Action(damage=self.getDamage(15), strength=3)
        }
        if self.checkMoveQueueThree("laser"):
            action = "claw"
        elif self.checkMoveQueueThree("claw"):
            action = "laser"
        else:
            chance = random.randint(0, 100)
            if chance < 60:
                action = "laser"
            else:
                action = "claw"
        if action == "laser":
            self.burn_count += 2

        chance = random.randint(0, 100)
        if chance < ((self.burn_count/(self.burn_count + 30)) * 5):
            actions[action].damage += 2
        self.updateQueue(action)
        return actions[action]


class Repulsor(Monster):

    def getAction(self):
        actions = {
            "attack": Action(damage=11),
            "daze": Action()
        }
        if self.checkMoveQueueTwo("attack"):
            action = "daze"
        else:
            chance = random.randint(0, 100)
            if chance < 80:
                action = "daze"
            else:
                action = "attack"
        self.updateQueue(action)
        return actions[action]

class ShelledParasite(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(ShelledParasite, self).__init__(name, health, strength, dex)
        self.armour = 14
        self.stunned = False

    def getAction(self):
        actions = {
            "double strike": Action(damage=7, hits=2),
            "suck": Action(damage=10),
            "fell": Action(damage=18, frail=2)
        }
        if self.turns == 1:
            chance = random.randint(0, 100)
            if chance < 50:
                action = "double strike"
            else:
                action = "suck"
        elif self.stunned:
            self.stunned = False
            self.updateQueue("stunned")
            return Action()
        else:
            double_strike_chance = 40
            suck_chance = 40
            if self.checkMoveQueueTwo("fell"):
                double_strike_chance = 50
                suck_chance = 100
            elif self.checkMoveQueueThree("double strike"):
                double_strike_chance = -1
                suck_chance = 60
            elif self.checkMoveQueueThree("suck"):
                double_strike_chance = 60
                suck_chance = -1

            chance = random.randint(0, 100)
            if chance < double_strike_chance:
                action = "double strike"
            elif chance < suck_chance:
                action = "suck"
            else:
                action = "fell"
        
        if action == "suck":
            self.health += 10
        if self.armour > 0:
            actions[action].block = self.armour

        self.updateQueue(action)
        return actions[action]

    def takeDamage(self, damage, hits=1, attacker=None):

        for hit in range(0, hits):
            super(ShelledParasite, self).takeDamage(damage, 1, attacker)
            if self.block <= 0 and self.armour > 0:
                self.armour -= 1

            if self.armour <= 0:
                self.stunned = True
                self.armour = -1
                

class SnakePlant(Monster):

    def getAction(self):
        actions = {
            "spores": Action(frail=2, weak=2),
            "chomp": Action(damage=7, hits=3)
        }
        
        if self.checkMoveQueueThree("chomp"):
            action = "spores"
        elif self.checkMoveQueueTwo("spores"):
            action = "chomp"
        else:
            chance = random.randint(0, 100)
            if chance < 65:
                action = "chomp"
            else:
                action = "spores"
        self.updateQueue(action)
        return actions[action]

    def takeDamage(self, damage, hits=1, attacker=None):
        super(SnakePlant, self).takeDamage(damage, hits, attacker)
        self.block = 3 + (hits - 1)


class Spiker(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(Spiker, self).__init__(name, health, strength, dex)
        self.thorns = 3
        self.buff_count = 0

    def getAction(self):
        actions = {
            "attack": Action(damage=7),
            "buff": Action()
        }
        if self.buff_count == 6:
            action = "attack"
        elif self.checkMoveQueueThree("attack"):
            action = "buff"
        else:
            chance = random.randint(0, 100)
            if chance < 50:
                action = "attack"
            else:
                action = "buff"

        if action == "buff":
            self.thorns += 2

        self.updateQueue(action)
        return actions[action]


class Snecko(Monster):

    def getAction(self):
        actions = {
            "tail whip": Action(damage=8, vulnerable=2),
            "bite": Action(damage=15)
        }

        if self.turns == 1:
            return Action()
        else:
            if self.checkMoveQueueThree("bite"):
                action = "tail whip"
            else:
                chance = random.randint(0, 100)
                if chance < 40:
                    action = "tail whip"
                else:
                    action = "bite"
        
        self.updateQueue(action)
        return actions[action]


class SphericGuardian(Monster):
    
    def __init__(self, name, health, strength=0, dex=0):
        super(SphericGuardian, self).__init__(name, health, strength, dex)
        self.artifact = 3
        self.block = 40

    def startTurn(self):
        self.turns += 1

    def getAction(self):
        actions = {
            "activate": Action(block=20),
            "attack": Action(damage=10, frail=5),
            "slam": Action(damage=10, hits=2),
            "harden": Action(damage=10, block=15)
        }
        if self.turns == 1:
            action = "activate"
        elif self.turns == 2:
            action = "attack"
        elif self.turns % 2 == 1:
            action = "slam"
        else:
            action = "harden"

        self.updateQueue(action)
        return actions[action]

class SpireGrowth(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(SpireGrowth, self).__init__(name, health, strength, dex)
        self.constrict_turns = 0

    def getAction(self):
        actions = {
            "quick tackle": Action(damage=16),
            "smash": Action(damage=22),
            "constrict": Action(),
        }

        if self.constrict_turns == 3:
            action = "smash"
        elif self.constrict_turns > 0:
            if self.checkMoveQueueThree("smash"):
                action = "quick tackle"
            elif self.checkMoveQueueThree("quick tackle"):
                action = "smash"
            else:
                chance = random.randint(0, 100)
                if chance < 50:
                    action = "quick tackle"
                else:
                    action = "smash"
        else:
            chance = random.randint(0, 100)
            if self.checkMoveQueueThree("quick tackle") or chance < 50:
                action = "constrict"
                self.constrict_turns = 3
            else:
                action = "quick tackle"

        if self.constrict_turns == 1 or self.constrict_turns == 2:
            actions[action].damage += 10
        self.updateQueue(action)
        return actions[action]

    def endTurn(self):
        super(SpireGrowth, self).endTurn()
        if self.constrict_turns > 0:
            self.constrict_turns -= 1


class Transient(Monster):

    def getAction(self):
        if self.turns == 5:
            self.runaway = True
        
        damage = 30 + ((self.turns - 1) * 10)
        return Action(damage=damage)


class WrithingMass(Monster):

    def __init__(self, name, health, strength=0, dex=0):
        super(WrithingMass, self).__init__(name, health, strength, dex)
        self.moveQueue.append('')

    def getAction(self):
        actions = {
            "defend": Action(damage=15, block=16),
            "debuff": Action(damage=10, weak=2, vulnerable=2),
            "attack_one": Action(damage=7, hits=3),
            "attack_two": Action(damage=32)
        }
        action = self.moveQueue[0]

        while action == self.moveQueue[0]:
            chance = random.randint(0, 100)
            if chance < 32:
                action == "defend"
            elif chance < 54:
                action = "debuff"
            elif chance < 86:
                action = "attack_one"
            else:
                action = "attack_two"

        self.updateQueue(action)
        return actions[action]

    def takeDamage(self, damage, hits=1, attacker=None):
        super(WrithingMass, self).takeDamage(damage, hits, attacker)
        self.block = 3 + (hits - 1)
