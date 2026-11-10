#Welcome the player
print("===ESCAPE THE CASTLE===")
print("Welcome, adventurer!")

#Get the player name, age and character class
charName = input("What is it that people call you? ")
charAge = int(input("How many years have you lived? "))
charClass = input("What class do you wish to be?")

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
print(f"\n{charName} ,you find yourself beatX and bruised in a dark damp castle") 
print("  You hear the sound of fooststeps appoaching, you must make a decision quickly!")
print("  Your adventure begins now, choose wisely and you may escape the castle alive!")