import logging
import copy

from monsters.gremlin import *
from monsters.slavers import *
from monsters.misc import *
from monsters.bandits import *
from monsters.elites import *
from monsters.slimes import *

from utils import print_message

MONSTERS = {
        "Blue Slaver": BlueSlaver("Blue Slaver", 46),
        "Red Slaver": RedSlaver("Red Slaver", 46),
        "Taskmaster": Taskmaster("Taskmaster", 54),
        "Mad Gremlin": MadGremlin("Mad Gremlin", 20),
        "Gremlin Wizard": GremlinWizard("Gremlin Wizard", 21),
        "Fat Gremlin": FatGremlin("Fat Gremlin", 13),
        "Shield Gremlin": ShieldGremlin("Shield Gremlin", 12),
        "Sneaky Gremlin": SneakyGremlin("Sneaky Gremlin", 10),
        "Gremlin Leader": GremlinLeader("Gremlin Leader", 140),
        "Gremlin Nob": GremlinNob("Gremlin Nob", 82),
        "Cultist": Cultist("Cultist", 48),
        "Centurion": Centurion("Centurion", 76),
        "Jaw Worm": JawWorm("Jaw Worm", 40),
        "Fungi Beast": FungiBeast("Fungi Beast", 22),
        "Red Louse": RedLouse("Red Louse", 10),
        "Green Louse": GreenLouse("Green Louse", 11),
        "Bear": Bear("Bear", 38),
        "Romeo": Romeo("Romeo", 35),
        "Pointy": Pointy("Pointy", 30),
        "Mugger": Mugger("Mugger", 48),
        "Looter": Looter("Looter", 44),
        "Byrd": Byrd("Byrd", 25),
        "Chosen": Chosen("Chosen", 95),
        "Darkling": Darkling("Darkling", 48),
        "Exploder": Exploder("Exploder", 30),
        "The Maw": TheMaw("The Maw", 300),
        "Mystic": Mystic("Mystic", 48),
        "Orb Walker": OrbWalker("Orb Walker", 90),
        "Repulsor": Repulsor("Repulsor", 29),
        "Shelled Parasite": ShelledParasite("Shelled Parasite", 68),
        "Snake Plant": SnakePlant("Snake Plant", 75),
        "Spiker": Spiker("Spiker", 42),
        "Snecko": Snecko("Snecko", 114),
        "Spheric Guardian": SphericGuardian("Spheric Guardian", 20),
        "Spire Growth": SpireGrowth("Spire Growth", 170),
        "Transient": Transient("Transient", 999),
        "Writhing Mass": WrithingMass("Writhing Mass", 160),
        "Book Of Stabbing": BookOfStabbing("Book Of Stabbing", 150),
        "Giant Head": GiantHead("Giant Head", 500),
        "Lagavulin": Lagavulin("Lagavulin", 109),
        "Nemesis": Nemesis("Nemesis", 185),
        "Sentry": Sentry("Sentry", 38),
        "Spire Shield": SpireShield("Spire Shield", 110),
        "Spire Spear": SpireSpear("Spire Spear", 160),
        "Reptomancer": Reptomancer("Reptomancer", 180),
        "Small Acid Slime": SmallAcidSlime("Small Acid Slime", 8),
        "Medium Acid Slime": MediumAcidSlime("Medium Acid Slime", 28),
        "Large Acid Slime": LargeAcidSlime("Large Acide Slime", 65),
        "Small Spike Slime": SmallSpikeSlime("Small Spike Slime", 10),
        "Medium Spike Slime": MediumSpikeSlime("Medium Spike Slime", 28),
        "Large Spike Slime": LargeSpikeSlime("Large Spike Slime", 64)
    }

def takeTurn(attacker, defender):
    attacker.startTurn()

    actions = attacker.getAction()
    if not isinstance(actions, list):
        actions = [actions]

    for action in actions:
        if action.damage is not None:
            defender.takeDamage(action.damage, action.hits, attacker)
        if action.weak is not None:
            defender.makeWeak(action.weak)
        if action.vulnerable is not None:
            defender.makevulnerable(action.vulnerable)
        if action.frail is not None:
            defender.makeFrail(action.frail)
        if action.remove_dex is not None:
            defender.removeDex(action.remove_dex)
        if action.remove_strength is not None:
            defender.removeStrength(action.remove_strength)
        if action.block is not None:
            attacker.addBlock(action.block)
        if action.strength is not None:
            attacker.addStrength(action.strength)

    attacker.endTurn()


def fight(attacker, defender, iterations=1000):
    wins = [0,0]
    for x in range(0,iterations):
        monster_one = copy.deepcopy(MONSTERS[attacker])
        monster_two = copy.deepcopy(MONSTERS[defender])
        while not monster_one.ran_away() and not monster_two.ran_away():
            takeTurn(monster_one, monster_two)
            if not monster_two.isAlive():
                logging.debug("{} wins".format(monster_one.name))
                wins[0] += 1
                break
            if not monster_one.isAlive():
                logging.debug("{} wins".format(monster_two.name))
                wins[1] += 1
                break

            takeTurn(monster_two, monster_one)
            if not monster_one.isAlive():
                logging.debug("{} wins".format(monster_two.name))
                wins[1] += 1
                break

            if not monster_two.isAlive():
                logging.debug("{} wins".format(monster_one.name))
                wins[0] += 1
                break

            logging.debug("{} {}".format(monster_one, monster_two))
        

    logging.debug("{}: {} wins".format(attacker, wins[0]))
    logging.debug("{}: {} wins".format(defender, wins[1]))

    return wins[0]

def convertToCSV(results):
    headers = results.keys()
    headers.sort()
    with open("results.csv", "w") as f:
        f.write(",{}\n".format(",".join(headers)))
        for monster in headers:
            monster_results = results[monster]
            f.write("{},{}\n".format(monster, ",".join([str(monster_results[header]) for header in headers])))

def main():
    monsters = MONSTERS.keys()
    results = {}
    for attacker in monsters:
        logging.critical("Starting {}".format(attacker))
        for defender in monsters:
            logging.critical("{} V {}".format(attacker, defender))
            wins = fight(attacker, defender)
            if attacker not in results:
                results[attacker] = {}
            results[attacker][defender] = wins
    
    logging.critical(results)
    convertToCSV(results)

logging.basicConfig(level=logging.CRITICAL)

main()

# fight("Large Acid Slime", "The Maw", 1)
