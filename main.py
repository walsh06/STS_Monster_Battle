from monster import FatGremlin, GremlinWizard, MadGremlin, BlueSlaver, RedSlaver, Cultist
from utils import print_message

def takeTurn(attacker, defender):
    action = attacker.getAction()
    if action.damage is not None:
        defender.takeDamage(action.damage)
    if action.weak is not None:
        defender.makeWeak(action.weak)
    if action.vunerable is not None:
        defender.makeVunerable(action.vunerable)

    attacker.endTurn()

def getMonster(name):
    monsters = {
        "Blue Slaver": BlueSlaver("Blue Slaver", 46, 0, 0),
        "Red Slaver": RedSlaver("Red Slaver", 46, 0, 0),
        "Mad Gremlin": MadGremlin("Mad Gremlin", 20, 0, 0),
        "Gremlin Wizard": GremlinWizard("Gremlin Wizard", 21, 0, 0),
        "Fat Gremlin": FatGremlin("Fat Gremlin", 13, 0, 0),
        "Cultist": Cultist("Cultist", 48, 0, 0)
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
                print_message("{} wins".format(monster_one.name))
                wins[0] += 1
                break
            
            takeTurn(monster_two, monster_one)
            if not monster_one.isAlive():
                print_message("{} wins".format(monster_two.name))
                wins[1] += 1
                break

            print_message("{} {}".format(monster_one, monster_two))
    
    print_message("{}: {} wins".format(attacker, wins[0]), True)
    print_message("{}: {} wins".format(defender, wins[1]), True)

    return wins[0]

def convertToCSV(results):
    headers = results.keys()
    with open("results.csv", "w") as f:
        f.write(",{}\n".format(",".join(headers)))
        for monster in headers:
            monster_results = results[monster]
            f.write("{},{}\n".format(monster, ",".join([str(monster_results[header]) for header in headers])))

def main():
    monsters = ("Blue Slaver", "Red Slaver", "Mad Gremlin", "Fat Gremlin", "Gremlin Wizard", "Cultist")
    results = {}
    for attacker in monsters:
        for defender in monsters:
            wins = fight(attacker, defender)
            if attacker not in results:
                results[attacker] = {}
            results[attacker][defender] = wins
    
    print results
    convertToCSV(results)

main()

#fight("Cultist", "Red Slaver", 1)