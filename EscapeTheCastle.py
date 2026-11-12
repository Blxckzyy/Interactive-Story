import random

#Welcome the player
print("===ESCAPE THE CASTLE===")
print("Welcome, adventurer!")

#Get the player name, age and character class
charName = input("\nWhat is it that people call you? ")
charAge = int(input("\nHow many years have you lived? "))
charClass = input("\nWhat type of adventurer are you? ")

#Set starting values
health = 3
gold = 20
hasKey = False

#Display the character profile
print("\n=== YOUR CHARACTER ===")
print(f"Name: {charName}")
print(f"Age: {charAge}")
print(f"Class: {charClass}")
print(f"Health: {health}")
print(f"Gold: {gold}")
print(f"Has Key: {hasKey}")

#Begin the story
print(f"\n{charName} ,you find yourself beat and bruised in a dark damp castle") 
print("  You hear the sound of fooststeps appoaching, you must make a decision quickly!")
print("  Your adventure begins now, choose wisely and you may escape the castle alive!")



# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================


#Introduce the scene to the player
print("You wake up in a dark cell, you have no memory of how you got there.")
print("You can see a door, a window and an old bed in the corner of the room.")

#Ask the player what they want to investigate
#.lower() convets their answer to lowercase so that it can be compared to the options below
choice = input("What would you like to investigate? Will it be the door, window or bed? ").lower()

#Check whether the player has chosen the door, window or bed and respond accordingly
if choice == "door":
    print("You approach the door and see that it is locked. You will need to find a key to open it.")
elif choice == "window":
    print("You approach the window and see that it is barred. It won't open.")
elif choice == "bed":
    print("You approach the bed and see that it is old and dusty. You find a small iron key hidden under the pillow.")
else:
    print("You decide not to investigate anything and remain in the cell.")


# ==========================================
# ESCAPE THE CASTLE - SCENE 2: THE CORRIDOR
# ==========================================

#Create a list to hold the player's inventory
#We are assuming that the player has found the key in the previous scene, we will add it to their inventory
inventory = ["Iron Key"]

#Introduce the scene to the player
print("\nYou manage to unlock the door and step into a long, dark corridor.")
print("You notice an old wooden cabinet against the wall and a torch on the wall that is still burning.")

choice = input("What would you like to investigate the cabinet? (Yes/No) ").lower()

if choice == "yes":
    print("You open the cabinet and find a dull rusty dagger inside.")
    print("You take the rust dagger and add it to your inventory.")
    inventory.append("Rust Dagger")
elif choice == "no":
    print("You decide not to investigate the cabinet, leaving it closed and continue down the corridor.")

print(f"\nYour inventory now contains: {inventory}")

# ==========================================
# ESCAPE THE CASTLE - CORRIDOR ENCOUNTER
# ==========================================
 

def encounter(creature):
    print(f"A {creature} appears!!")

    if creature == "guard":
        print("The Guard draws their sword")

    elif creature == "ghost":
        print("The ghost floats towards you")
    elif creature == "sphinx":
        print("The Sphinx spots you and starts charging in your direction")

#define the corridor scene
def corridor():
    print("You walk down a dark castle corridor. \nYou hear a strange noise ahead...")

    creatures = ["Guard", "Ghost", "Sphinx"]

    random_creature = random.choice(creatures).lower()
    encounter(random_creature)

#Start the scene
corridor()


