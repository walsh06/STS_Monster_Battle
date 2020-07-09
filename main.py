import logging
import copy

from monsters.gremlin import FatGremlin, GremlinWizard, MadGremlin, ShieldGremlin, SneakyGremlin
from monsters.slavers import BlueSlaver, RedSlaver
from monsters.misc import Cultist, Centurion, JawWorm, FungiBeast, RedLouse, GreenLouse, Byrd, Chosen, Darkling, Exploder, TheMaw, Mystic, OrbWalker, Repulsor
from monsters.bandits import Pointy, Romeo, Bear, Mugger, Looter

from utils import print_message

MONSTERS = {
        "Blue Slaver": BlueSlaver("Blue Slaver", 46),
        "Red Slaver": RedSlaver("Red Slaver", 46),
        "Mad Gremlin": MadGremlin("Mad Gremlin", 20),
        "Gremlin Wizard": GremlinWizard("Gremlin Wizard", 21),
        "Fat Gremlin": FatGremlin("Fat Gremlin", 13),
        "Shield Gremlin": ShieldGremlin("Shield Gremlin", 12),
        "Sneaky Gremlin": SneakyGremlin("Sneaky Gremlin", 10),
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
        "Repulsor": Repulsor("Repulsor", 29)
    }

def takeTurn(attacker, defender):
    attacker.startTurn()

    action = attacker.getAction()
    if action.damage is not None:
        defender.takeDamage(action.damage, action.hits)
    if action.weak is not None:
        defender.makeWeak(action.weak)
    if action.vulnerable is not None:
        defender.makevulnerable(action.vulnerable)
    if action.frail is not None:
        defender.makeFrail(action.frail)
    if action.remove_dex is not None:
        defender.removeDex(action.remove_dex)
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
        while monster_one.isAlive() and monster_two.isAlive():
            takeTurn(monster_one, monster_two)
            if not monster_two.isAlive():
                logging.debug("{} wins".format(monster_one.name))
                wins[0] += 1
                break
            
            takeTurn(monster_two, monster_one)
            if not monster_one.isAlive():
                logging.debug("{} wins".format(monster_two.name))
                wins[1] += 1
                break

            logging.debug("{} {}".format(monster_one, monster_two))
        
        # special case where the exploder exploded but failed to kill
        # award win to the survivor
        if monster_two.name == "Exploder" and not monster_two.isAlive():
            logging.debug("{} wins".format(monster_one.name))
            wins[0] += 1
            break

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

#fight("Mystic", "Blue Slaver", 1)
