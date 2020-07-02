import logging

from monster import Monster, FatGremlin, GremlinWizard, MadGremlin, BlueSlaver, RedSlaver, Cultist, Pointy, Centurion, JawWorm
from utils import print_message

def takeTurn(attacker, defender):
    attacker.startTurn()

    action = attacker.getAction()
    if action.damage is not None:
        defender.takeDamage(action.damage, action.hits)
    if action.weak is not None:
        defender.makeWeak(action.weak)
    if action.vunerable is not None:
        defender.makeVunerable(action.vunerable)
    if action.block is not None:
        attacker.addBlock(action.block)
    if action.strength is not None:
        attacker.addStrength(action.strength)
    attacker.endTurn()

def getMonster(name):
    monsters = {
        "Blue Slaver": BlueSlaver("Blue Slaver", 46, 0, 0),
        "Red Slaver": RedSlaver("Red Slaver", 46, 0, 0),
        "Mad Gremlin": MadGremlin("Mad Gremlin", 20, 0, 0),
        "Gremlin Wizard": GremlinWizard("Gremlin Wizard", 21, 0, 0),
        "Fat Gremlin": FatGremlin("Fat Gremlin", 13, 0, 0),
        "Cultist": Cultist("Cultist", 48, 0, 0),
        "Pointy": Pointy("Pointy", 30, 0, 0),
        "Centurion": Centurion("Centurion", 76, 0, 0),
        "Jaw Worm": JawWorm("Jaw Worm", 40, 0, 0)
    }
    return monsters[name]


def fight(attacker, defender, iterations=1000):

    wins = [0,0]
    for x in range(0,iterations):
        monster_one = getMonster(attacker)
        monster_two = getMonster(defender)
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
    
    logging.debug("{}: {} wins".format(attacker, wins[0]))
    logging.debug("{}: {} wins".format(defender, wins[1]))

    return wins[0]

def convertToCSV(results):
    headers = results.keys()
    with open("results.csv", "w") as f:
        f.write(",{}\n".format(",".join(headers)))
        for monster in headers:
            monster_results = results[monster]
            f.write("{},{}\n".format(monster, ",".join([str(monster_results[header]) for header in headers])))

def main():
    monsters = ("Blue Slaver", "Red Slaver", "Mad Gremlin", "Fat Gremlin", "Gremlin Wizard", "Cultist", "Pointy", "Centurion", "Jaw Worm")
    results = {}
    for attacker in monsters:
        for defender in monsters:
            wins = fight(attacker, defender)
            if attacker not in results:
                results[attacker] = {}
            results[attacker][defender] = wins
    
    logging.critical(results)
    convertToCSV(results)

logging.basicConfig(level=logging.DEBUG)

main()

# fight("Cultist", "Jaw Worm", 1)
