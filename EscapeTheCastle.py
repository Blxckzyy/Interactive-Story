import random
import sys
#Set starting values
health = 3
gold = 20
hasKey = False
inventory = []
#Welcome the player

def game_over():
    print("\nGame Over. Thanks for playing Escape the Castle!")
    sys.exit()  # Immediately stops the entire Python program

def win_screen():
    print("\nYou have successfully Escaped the Castle. Congratulations!")
    sys.exit()  # Immediately stops the entire Python program

def introduction():
    print("\n\n===ESCAPE THE CASTLE===")
    print("Welcome, adventurer!")

    #Get the player name, age and character class
    charName = input("\nWhat is it that people call you? ")
    charAge = int(input("\nHow many years have you lived? "))
    charClass = input("\nWhat type of adventurer are you? ")



    #Display the character profile
    print("\n=== YOUR CHARACTER ===")
    print(f"Name: {charName}")
    print(f"Age: {charAge}")
    print(f"Class: {charClass}")
    print(f"Health: {health}")
    print(f"Gold: {gold}")
    print(f"Has Key: {hasKey}")

    # Begin the story
    print(f"\n{charName}, your eyes flutter open. You are battered, bruised, and lying on the cold stone floor of a dark, damp castle.")
    print("Your adventure begins now. Choose wisely, and you might just escape this place alive...")


def cell(hasKey):
    # ==========================================
    # ESCAPE THE CASTLE - SCENE 1: THE CELL
    #===========================================
    # Introduce the scene to the player
    print("\n\nPanic sets in as you realize you have no memory of how you got here.")
    print("As your eyes adjust to the gloom, you spot a heavy wooden door, a high barred window, and an old, rotting bed in the corner.")
    print("Suddenly, the heavy thud of approaching footsteps echoes down the corridor outside. You need to act fast!")
    #Ask the player what they want to investigate
    #.lower() convets their answer to lowercase so that it can be compared to the options below
    while hasKey == False:
        choice = input("\nWhat would you like to investigate? Will it be the door, window or bed? ").lower()

        #Check whether the player has chosen the door, window or bed and respond accordingly
        if choice == "door":
            print("You approach the door and see that it is locked. You will need to find a key to open it.")
        elif choice == "window":
            print("You approach the window and see that it is barred. It won't open.")
        elif choice == "bed":
            print("You approach the bed and see that it is old and dusty.\nYou find a small iron key hidden under the pillow.")
            inventory.append("Iron Key")
            hasKey = True
        else:
            print("You decide not to investigate anything and remain in the cell.")
            break
    print("\nYou unlocked the cell door")
    print("You step out into the corridor.")
    print(f"Your inventory: {inventory}")

    # ==========================================
    # ESCAPE THE CASTLE - SCENE 2: THE CORRIDOR
    # ==========================================

    #Create a list to hold the player's inventory
    #We are assuming that the player has found the key in the previous scene, we will add it to their inventory


    #Introduce the scene to the player
    print("\nYou manage to unlock the door and step into a long, dark corridor.")
    print("You notice an old wooden cabinet against the wall and a torch on the wall that is still burning.")

    choice = input("\nWhat would you like to investigate the cabinet? (Yes/No) ").lower()

    if choice == "yes":
        print("\nYou open the cabinet and find a dull rusty dagger inside.")
        print("You take the rust dagger and add it to your inventory.")
        inventory.append("Rust Dagger")
    elif choice == "no":
        print("\nYou decide not to investigate the cabinet, leaving it closed and continue down the corridor.")

    print(f"\nYour inventory now contains: {inventory}")






def corridor_encounter():
        # ==========================================
    # ESCAPE THE CASTLE - CORRIDOR ENCOUNTER
    # ==========================================
 #define the corridor scene
    print("You walk down a dark castle corridor. \nYou hear a strange noise ahead...")

    creatures = ["Guard", "Ghost", "Sphinx"]

    random_creature = random.choice(creatures).lower()

    print(f"\nA {random_creature} appears!!")

    if random_creature == "guard":
        print("\nThe Guard draws their sword and charges towards you!")

    elif random_creature == "ghost":
        print("\nThe ghost floats towards you!")
    elif random_creature == "sphinx":
        print("\nThe Sphinx spots you and starts charging in your direction!")


def clueBook():
    print("To pass the final threshold, name the servant that follows you in the torchlight, grows tall at dusk, yet vanishes the moment you step into pitch darkness.")
def library_choice():
    while True:
        choice2 = input("\nYou stumble across a book that is lay on a dusty table, would you like to read it? (Yes/No) ").lower()
        if choice2 == "yes":
            clueBook()
            print("\nYou wonder what this could mean and take it with you.")
            inventory.append("Mysterious book")
            print(f"Your inventory now holds: {inventory}")
            break  # Stops the loop once they read and take the book
        else:
            print("\nYou think this book could be an important item.")
            print("Maybe you should take another look")
            # Because there is no 'break' here, the loop goes back to the top and asks again!
def library():
    print("\nAfter continuing down the corridor, you are faced with a heavy door that you manage to open just enough to fit through the crack.")
    print("A vast library spans as far as your eye can see.")
    choice = input("\nWould you like to explore the library too see if there will be a clue to escape? (Yes/No) ").lower()
    if choice == "yes":
        library_choice()
    elif choice == "no":
        print("\nYou move past the library, but you can't shake this feeling of curiosity.")
        choice3 = input("Do you let your curiosity get the better of you? (Yes/No) ").lower()
        if choice3 == "yes":
            library_choice()
        else:
            print("You get attacked by a Guard from behind.")
            print("Running out of breath and bleeding out on the floor, your eyes slowly begin to close.")
            game_over()

def castle_gate():
    print("\nYou leave the library and carry on down the long corridor")
    print("You notice 2 dimply lit torches flickering in the stale air")
    print("Guard: Halt! I dont know how you got here, but i will only let you pass if you tell me the correct password")
    answer = input("So what is it? ").lower()
    while answer != "shadow":
        if answer == "shadow":
            win_screen()
        elif answer != "shadow":
            print("That is incorrect!")
            print("Would you like to:\nA: Try Again\nB:Read your book")
            choice = input("Type 'A' for try again\nType 'B' to read your book\n").upper()
            if choice == "A":
                print("Guard: Halt! I dont know how you got here, but i will only let you pass if you tell me the correct password")
                answer = input("So what is it? ").lower()
            elif choice == "B":
                clueBook()
                print("Guard: Halt! I dont know how you got here, but i will only let you pass if you tell me the correct password")
                answer = input("So what is it? ").lower()
            else:
                print("Escape isn't an option")
    win_screen()


#Start the game

def playGame():
    introduction()
    cell(hasKey)
    corridor_encounter()
    library()
    castle_gate()

playGame()