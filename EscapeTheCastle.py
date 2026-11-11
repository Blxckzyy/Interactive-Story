#Welcome the player
print("===ESCAPE THE CASTLE===")
print("Welcome, adventurer!")

#Get the player name, age and character class
charName = input("What is it that people call you? ")
charAge = int(input("How many years have you lived? "))
charClass = input("What type of adventurer are you? ")

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
    print("You approach the bed and see that it is old and dusty. You find a small key hidden under the pillow.")
else:
    print("You decide not to investigate anything and remain in the cell.")