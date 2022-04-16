# Written by Daniel C
# Graphing Calculator Edition

from random import randint
from time import sleep
from sys import exit

class Player:
    """The object that represents the player, storing its HP, damage, and heal amount.
    Contains various methods to attack enemies, take damage from enemies, and recover."""
    def __init__(self, hp:int=100, dmg:int=20, heal:int=15, points:int=0) -> None:
        # Base stats
        self.hp = hp
        self.max_hp = hp
        self.dmg = dmg
        self.heal = heal
        self.points = points

        # State checkers
        self.dodged = False
        self.poisoned = False

        # Poison
        self.poisonDamage = 0
        self.poisonedTurns = 0
    
    def takeDamage(self, damage:int) -> None:
        """Causes the player to take damage from an enemy.
        The player has a flat 15% chance of dodging the attack."""
        if randint(1, 100) <= 85:
            self.hp -= damage
            print("You took {} damage!".format(damage))
            self.dodged = False
        else:
            print("You dodged the attack!")
            self.dodged = True
        sleep(1)
    
    def recover(self) -> None:
        """Recovers health when called by player input."""
        self.hp += self.heal
        print("You recovered {} HP!".format(self.heal))
        if self.poisoned:
            sleep(1)
            print("You cured the poison!")
            self.poisoned = False
            self.poisonedTurns = 0
        sleep(1)
    
    def attack(self, enemy) -> None:

        """Attacks a single enemy.
        An attack causes the targeted enemy to take damage, with the method giving the player's damage a ±10% deviation.
        The player has a 20% chance of a critical hit, which grants a 1.5x damage multiplier."""
        if randint(1, 10) < 9:
            damage = randint(int(self.dmg*0.9), int(self.dmg*1.1))
        else:
            print("You got a critical hit!")
            sleep(1)
            damage = int(1.5*randint(int(self.dmg*0.9), int(self.dmg*1.1)))
        enemy.takeDamage(damage)
    
    def takePoisonDamage(self):
        """Inflicts damage on the player after the end of every enemy turn."""
        self.hp -= self.poisonDamage
        print("You took {} damage from poison!".format(self.poisonDamage))
        self.poisonedTurns += 1
        sleep(1)

class Enemy:
    """The generic class for an enemy. It is to be inherited by classes for specific enemies.
    This class itself should only be called for testing purposes."""
    def __init__(self, name:str, hp:int, dmg:int):
        self.name = name
        self.hp = hp
        self.dmg = dmg

    def display(self):
        """Returns the enemy's name and HP."""
        return "{}: {} HP".format(self.name, self.hp)
    
    def takeDamage(self, damage:int):
        """Called by player.attack() to inflict damage on the enemy."""
        self.hp -= damage
        print("You inflicted {} damage on {}!".format(damage, self.name))
        sleep(1)
    
    def attack(self, player:Player):
        """Attacks the player, with a ±10% deviation of its damage."""
        print(self.name, "attacks!")
        damage = randint(int(self.dmg*0.9), int(self.dmg*1.1))
        sleep(1)
        player.takeDamage(damage)
    
    def move(self, player, wave=None):
        """Goes through random number generation to determine the move
        that the enemy will take. By default, an enemy has a 100%
        chance of attacking due to the absence of other moves."""
        self.attack(player)

    # Define special methods here (such as buffs appling to all enemies).
    def spiderHeal(self):
        self.hp += 5

class Beetle(Enemy):

    def __init__(self, name):
        self.name = name
        self.hp = 30
        self.dmg = 12

    def applyArmor(self):
        """A healing mechanism for the beetle."""
        armour = 10
        self.hp += armour
        print("{} applied armour,\ngaining {} HP!".format(self.name, armour))
        sleep(1)
    
    def move(self, player, wave=None):
        """Beetles have a 20% chance of healing themselves with armour.
        Otherwise, they will simply attack."""
        if randint(1, 100) <= 80:
            self.attack(player)
        else:
            self.applyArmor()

class Spider(Enemy):
    def __init__(self, name):
        self.name = name
        self.hp = 50
        self.dmg = 22

    def healAll(self, wave):
        """The spider uses the entire wave and calls the special healing method
        defined in the Enemy class for every enemy in the wave."""
        for i in wave:
            i.spiderHeal()
        print("{} healed all enemies\nfor 5 health!".format(self.name))
        sleep(1)
    
    def move(self, player, wave):
        """There is a 15% chance of the spider healing every enemy. Otherwise,
        it will simply attack."""
        if randint(1, 100) <= 85:
            self.attack(player)
        else:
            self.healAll(wave)

class Wasp(Enemy):

    def __init__(self, name):
        self.name = name
        self.hp = 65
        self.dmg = 35
    
    def distracted(self):
        """A dummy method that makes the wasp not attack the player because wasps
        suck. This also tempers their high damage and health."""
        print("{} is distracted by food!".format(self.name))
        sleep(1)
    
    def move(self, player, wave=None):
        """The wasp has a 20% chance of getting distracted. Otherwise it will
        attack."""
        if randint(1, 5) == 3:
            self.distracted()
        else:
            self.attack(player)

class Mosquito(Enemy):

    def __init__(self, name):
        self.name = name
        self.hp = 300
        self.dmg = 55

    def distracted(self):
        """Another dummy method that causes those stupid mosquitos to get distracted."""
        print("{} is attracted by\nanother animal!".format(self.name))
        sleep(1)
    
    def poisonPlayer(self, player):
        """Causes the player to get poisoned, making them take damage over two turns."""
        print("You've been poisoned!")
        player.poisoned = True
        player.poisonDamage = int(self.dmg/4)
        sleep(1)
    
    def move(self, player, wave=None):
        """Mosquitos hit pretty hard and have a chance of poisoning the player.
        However, like wasps, they are easily distracted by other people they
        can bite. They have a 33% chance of getting distracted, otherwise they will attack."""
        if randint(1, 3) == 2:
            self.distracted()
        else:
            self.attack(player)
            if randint(1,2) == 2 and player.dodged == False:
                self.poisonPlayer(player)
            
class Lose(Exception):
    """This exception is raised when the player reaches zero health,
    ending the game immediately."""
    pass

def clearShell():
    """Clears the terminal by adding newline statements for calculator compatibility."""
    print("\n\n\n\n\n\n\n\n\n")

def titleScreen():
    """Logic for the title screen. If the word GODMODE is inputted when exiting the help and credits, the player recieves infinite stats."""
    checker = False

    while True:
        print("""
Python Dungeon
Graphing Calculator Edition

[1] PLAY
[2] HELP AND CREDITS
[3] EXIT
    """)

        option = input("Select option (default 2): ").strip()
        if option == "1":
            break
        elif option == "3":
            exit()
        else:
            clearShell()
            print("[ENTER] Next Line")
            help = """
INTRODUCTION

Welcome to Python Dungeon, a simple
turn-based strategy game built
entirely in Python!
Here, you will go off to
fight the bugs that
plague your coding success.
As you go through the dungeon,
you will see new bugs, each
increasing in strength.
Your goal is to get to the end of
the dungeon, defeating all the
bugs in your way so that your code
can finally work!

CHANGELOG

V2.1.1TI Beta Hotfix 1
- Created a more easily scrollable
credits section
- Fixed a bug in Godmode's numbers
being too large

V2.1.1TI Beta
- First version of Python Dungeon
optimized for use with calculators

V2.1.1 Beta
- Swapped the match-case statements
for if statements to improve
backwards-compatibility

V2.1 Beta
- Created a new mosquito enemy,
alongside a poison mechanic which
affects the player
- Added dodge checking so that
some effects on the player don't
engage if an attack is dodged
- Compacted the main() function
- Added a new wave which features
the mosquito

CREDITS

Base code programmed by Daniel C,
Grade 11
Originally a creative experience
as part of the IB CAS Program

Originally finished on
December 12, 2021
First pushed to GitHub on
January 29, 2022

Thank you for playing!
""".splitlines()

            for line in help:
                print(line, end="")
                input()
            print("\n[ENTER] BACK TO TITLE")
            checker = input()
            if checker == "GODMODE": checker = True
            clearShell()
    return checker

def combatWave(waveNum, player, beetles, spiders, wasps, mosquitos, lastRound=False):
    """The logic for a wave of combat, repeating infinitely until
    either the wave is cleared or the player is defeated."""

    # Initialize the wave, placing enemy objects into a list.
    wave = []
    for i in range(1, beetles+1):
        wave.append(Beetle("Beetle {}".format(i)))
    for i in range(1, spiders+1):
        wave.append(Spider("Spider {}".format(i)))
    for i in range(1, wasps+1):
        wave.append(Wasp("Wasp {}".format(i)))
    for i in range(1, mosquitos+1):
        wave.append(Mosquito("Mosquito {}".format(i)))
    
    # Infinitely loop while the wave is still active.
    while True:
        clearShell()
        # Print the UI, including all of the enemies and their
        # respective HPs.
        print("""
WAVE {}

ENEMIES:
""".format(waveNum))
        for i, j in enumerate(wave):
            print("[{}]".format(i+1), j.display())
        print("""
[1]: ATTACK
[2]: HEAL""")
        print("YOUR HP: {} HP".format(player.hp))
        while True:
            option = input("Please input an option: ").strip()
            if option == "1" or option == "2":
                break
            else:
                print("Invalid input.")
        if option == "1":
            while True:
                try:
                    # Attacks an enemy using the index that the user provides.
                    option = int(input("Select the enemy to attack: ").strip())
                    toAttack = wave[option-1]
                    player.attack(toAttack)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
                except IndexError:
                    print("Your input is out of range.")
            
            # Eliminates an enemy if its health is drained. Also checks if the wave
            # is cleared.
            if toAttack.hp <= 0:
                print("You eliminated {}!".format(toAttack.name))
                sleep(1)
                wave.pop(option-1)
                if len(wave) == 0:
                    clearShell()
                    print("WAVE CLEARED!")
                    break
        
        elif option == "2":
            player.recover()
        # Loops through the wave to allow all the enemies to move.
        for i in wave:
            i.move(player, wave)

        if player.poisoned:
            player.takePoisonDamage()
            if player.poisonedTurns == 2:
                print("The poison wore off!")
                player.poisoned = False
                player.poisonedTurns = 0
                sleep(1)

        # Raises the Lose exception if the player runs out of health.
        if player.hp <= 0:
            raise Lose

    if not lastRound:
        levelUp(player)

def levelUp(player):
    """Allows the player to upgrade their damage, health, and healing."""

    player.points += 3
    while player.points > 0:
        print("""
CHOOSE YOUR UPGRADES

[1] DAMAGE: +10 PER POINT
[2] HEALTH: +20 PER POINT
[3] HEALING: +10 PER POINT

[4] GO TO NEXT WAVE
You have {} upgrade point(s)
        """.format(player.points))
        while True:
            upgrade = input("Choose option: ").strip()
            if upgrade not in ["1", "2", "3", "4"]:
                print("Invalid upgrade option.")
            else:
                break
        if upgrade == "4":
            break

        while True:
            try:
                print("Input how many points you want")
                pointsToSpend = int(input("to spend on the upgrade: ").strip())
                while player.points < pointsToSpend:
                    print("You don't have enough points.\nYou currently have {} point(s).".format(player.points))
                    print("Input how many points you want")
                    pointsToSpend = int(input("to spend on the upgrade: ").strip())

                while pointsToSpend < 0:
                    print("Invalid input; please enter an integer from 0-{}".format(player.points))
                    print("Input how many points you want")
                    pointsToSpend = int(input("to spend on the upgrade: ").strip())
                break
            except ValueError:
                print("Please enter a valid integer.")

        if pointsToSpend == 0:
                print("Upgrade Cancelled.")

        else:
            if upgrade == "1":
                player.dmg += 10 * pointsToSpend
                print("Upgraded strength successfully!")

            elif upgrade == "2":
                player.max_hp += 20 * pointsToSpend
                print("Upgraded health successfully!")

            elif "3":
                player.heal += 10 * pointsToSpend
                print("Upgraded healing successfully!")
        
        sleep(1)
        clearShell()
        player.points -= pointsToSpend
    # Resets the player's health for the next wave.
    player.hp = player.max_hp

def main():
    """The main routine, infinitely looping until the user stops the game."""
    while True:
        godmode = titleScreen()
        try:
            if godmode:
                player = Player(69420, 69420, 69420)
            else:
                player = Player(120, 25, 35)
            combatWave(1, player, 2, 0, 0, 0)
            combatWave(2, player, 1, 2, 0, 0)
            combatWave(3, player, 0, 2, 1, 0)
            combatWave(4, player, 1, 2, 2, 0)
            combatWave(5, player, 2, 1, 3, 0)
            combatWave(6, player, 0, 0, 0, 1, True)

        except Lose:
            print("""
You were unable to keep up with all 
the bugs in your code. Maybe go
through another round of debugging?

[1] RETURN TO TITLE
[2] EXIT
""")
        else:
            print("""
Congratulations! You have completed
the Python Dungeon and your code
works once again!
    
Thanks for playing!

[1] RETURN TO TITLE
[2] EXIT
""")
    
        option = input("Select option: ").lower().strip()
        if option == "2":
            break

main()