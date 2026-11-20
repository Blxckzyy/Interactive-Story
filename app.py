import os
import streamlit as st
import random
from dotenv import load_dotenv
from google import genai

 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
 
client = genai.Client(api_key=api_key) if api_key else None
 
MODEL_NAME = "gemini-3.5-flash-lite"

# ================================================================
# 1. PAGE SETUP — SAME APPROACH AS THE FINAL APP
# ================================================================
# page_icon uses the Unicode castle character, not an image file.
# Keep this before other Streamlit display calls.


st.set_page_config(page_title="Escape the Castle", page_icon="🏰", layout="centered")
st.title("🏰 Escape the Castle")


# ================================================================
# 2. GAME SETUP — INITIALISE VALUES ONCE & STRUCTURED PROMPT
# ================================================================
# Session state remembers values when Streamlit reruns the script.

if "game_started" not in st.session_state:
    st.session_state.game_started = False

def start_game(name):
    st.session_state.game_started = True
    st.session_state.player_name = name
    st.session_state.health = 5
    st.session_state.max_health = 5
    st.session_state.inventory = []
    st.session_state.rooms = ["cell", "corridor", "crypt", "library", "guard_room", "dungeon", "castle_gate"]
    st.session_state.room_number = 0
    st.session_state.result_type= ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False

def restart_game():
    st.session_state.clear()
    st.rerun()

def get_current_room():
    return st.session_state.rooms[st.session_state.room_number]

def continue_game():
    st.session_state.result_type= ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False
    st.session_state.room_number += 1
    st.rerun()

def add_item(item):
        if item not in st.session_state.inventory:
            st.session_state.inventory.append(item)

def has_item(item):
    return item in st.session_state.inventory

def remove_item(item):
        if item in st.session_state.inventory:
            st.session_state.inventory(item)


def take_damage(amount):
    st.session_state.health = st.session_state.health - amount
    if st.session_state.health < 0:
        st.session_state.health = 0

def heal_player(amount):
    old_health = st.session_state.health
    st.session_state.health = min(st.session_state.max_health, st.session_state.health + amount)
    return st.session_state.health - old_health

def generate_story(room, action, outcome, fallback_message):
    if client is None:
        return fallback_message

    inventory_text = ", ".join(st.session_state.inventory)
    prompt = f"""
You are the storyteller for a dark fantasy
adventure game called Escape the Castle.
 
Player: {st.session_state.player_name}
Room: {room}
Health: {st.session_state.health}/{st.session_state.max_health}
Inventory: {inventory_text}
 
Action:
{action}
 
Outcome:
{outcome}
 
Describe what happens in 30-50 words.
 
Use second person.
Speak in a dark and mysterious tone/language
Do not change the outcome.
Do not change health or inventory.
Do not introduce new choices.
"""
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            generation_config={"thinking_level": "minimal"}
        )
        if interaction.output_text:
            return interaction.output_text
        return fallback_message
    except Exception as error:
        st.error(f"Gemini error: {error}")
        return fallback_message


def roll_dice():
    return random.randint(1,6)

def chance_encounter(button_text, room, action, success_number, success_outcome, success_fallback, failure_outcome, failure_fallback, damage, bonus_item = ""):
    if st.button(button_text):
        roll = roll_dice()
        if bonus_item != "" and has_item(bonus_item):
            roll = roll + 2
        if roll >= success_number:
            story = generate_story(room, action, success_outcome, success_fallback)
            set_result("success", story)
        else:
            take_damage(damage)
            story = generate_story(room, action, failure_outcome, failure_fallback)
            set_result("damage", story, damage)
        st.rerun()

# ================================================================
# 3. REUSABLE DISPLAY FUNCTIONS — KEEP EVERY ROOM CONSISTENT
# ================================================================

#Inventory management

#Showing the room
def show_room(title, description):
    st.header(title)
    st.write(description)


#Showing Player info
def show_player_info():
    st.subheader(f"👨 {st.session_state.player_name}")
    left, right = st.columns(2)
    with left:
        st.write(f"❤️ Health: {st.session_state.health} / {st.session_state.max_health}")
    with right:
        st.write(f"🎒 Inventory: {', '.join(st.session_state.inventory)}")
    st.caption(
        f"room {st.session_state.room_number +1}"
        f"of {len(st.session_state.rooms)}" 
    )
    st.divider()

def set_result(result_type, message, value = ""):
    st.session_state.result_type = result_type
    st.session_state.result_message = message
    st.session_state.result_value = value
    st.session_state.action_complete = True
    st.rerun()

def show_result():
    kind = st.session_state.result_type
    value = st.session_state.result_value
 
    if kind == "item":
        st.success(f"🎒 NEW ITEM: {value}")
    elif kind == "damage":
        st.error(f"💔 DAMAGE: You lose {value} health.")
    elif kind == "heal":
        st.success(f"💚 HEALED: You recover {value} health.")
    elif kind == "success":
        st.success("✅ Success!")
    else:
        st.info("The journey continues...")
 
    st.write(st.session_state.result_message)

def show_continue_button(text = "Continue"):
    if st.button(text):
        continue_game()



# ================================================================
# 4. START SCREEN — NAME INPUT FROM DAY 1
# ================================================================\

if "health" not in st.session_state:
    st.session_state.health = 5

if st.session_state.health <= 0:
    show_room("💀 Game Over", "Your strength gives out. The castle has claimed another victim.")
    st.error("You did not escape the castle")
    if st.button("🔄 Try Again"):
        restart_game()
    st.stop()


if not st.session_state.game_started:
    st.subheader("Create your character")
    playerName = st.text_input("What is your name? ")

    if st.button("Start your adventure!"):
        if playerName.strip():
            start_game(playerName)
            st.rerun()
        else:
            st.warning("Enter your name first before starting.")
else:
    show_player_info()
    room = get_current_room()

if st.session_state.game_started:
 
    # ============================================================
    # ROOM 1 — CELL (MODEL SIMPLE CONTINUE NAVIGATION)
    # ============================================================
    if room == "cell":
        show_room("🔒 The Cell", "You wake up in a dark cell. 3 walls and bars. The walls are crumbling around you.")
        if not st.session_state.action_complete:
            if st.button("🚪 Leave the cell"):
                outcome = "The player leaves the cell and enters the corridor."
                story = generate_story(
                    "The Cell", "leave the cell", outcome,
                    "You slip through the cell door and enter the corridor."
                )
                set_result("success", story)
        else:
            show_result()
            show_continue_button()

    # ============================================================
    # ROOM 2 — CORRIDOR (MODEL RESULT -> CONTINUE)
    # ============================================================
    elif room == "corridor":
        show_room("🕯️ The Corridor", "A wooden cabinet stands beside the staircase.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Search the cabinet"):
                    add_item("Rusty Dagger")
                    outcome = "The player finds a Rusty Dagger inside the cabinet."
                    story = generate_story(
                        "The Corridor", "search the cabinet", outcome,
                        "You find a Rusty Dagger inside the cabinet."
                    )
                    set_result("item", story, "Rusty Dagger")
            with right:
                if st.button("➡️ Ignore it"):
                    outcome = "The player leaves the cabinet and walks onwards."
                    story = generate_story(
                        "The Corridor", "ignore the cabinet", outcome,
                        "You leave the cabinet and walk onwards."
                    )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()  

    # ============================================================
    # ROOM 3 — CRYPT
    # ============================================================
    elif room == "crypt":
        show_room("⚰️ The Crypt", "A metal object glints beside a stone coffin.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Investigate the coffin"):
                    roll = roll_dice()
                    if roll >= 3:
                        add_item("Iron Key")
                        outcome = "The player finds an Iron Key inside the coffin."
                        story = generate_story(
                            "The Crypt", "investigate the coffin", outcome,
                            "You find an Iron Key inside the coffin."
                        )
                        set_result("item", story, "Iron Key")
                    else:
                        take_damage(1)

            with right:
                if st.button("🚪 Leave the crypt"):
                    outcome = "The player leaves the crypt and continues onwards."
                    story = generate_story(
                        "The Crypt", "leave the crypt", outcome,
                        "You leave the crypt and continue onwards."
                    )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()
 
    # ============================================================
    # ROOM 4 — LIBRARY
    # ============================================================
    elif room == "library":
        show_room("📚 The Forgotten Library", "A strange green light shines from an old book.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Read the old book"):
                    add_item("Mysterious Book")
                    outcome = (
                        "The player finds a clue in the book: a shadow follows in torchlight, "
                        "grows tall at dusk, and vanishes in complete darkness."
                    )
                    story = generate_story(
                        "The Forgotten Library", "read the old book", outcome,
                        "The book's clue reads: A shadow follows you in the torchlight, grows tall at dusk, "
                        "and vanishes in complete darkness."
                    )
                    set_result(
                        "item",
                        story,
                        "Mysterious Book",
                    )
            with right:
                if st.button("➡️ Leave the library"):
                    outcome = "The player leaves the library and continues onwards."
                    story = generate_story(
                        "The Forgotten Library", "leave the library", outcome,
                        "You leave the library and continue onwards."
                    )
                    set_result("story", story)
        else:
            show_result()
            show_continue_button()


    # ============================================================
    # ROOM 5 — The guard room
    # ============================================================
    elif room == "guard_room":
        show_room("⚔️ The Guard Room", "A ghostly knight blocks the doorway.")
        if "Rusty Dagger" in st.session_state.inventory:
            st.info("⚔️ You are carrying a Rusty Dagger.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("⚔️ Fight the knight"):
                    outcome = "The player defeats the knight and can continue."
                    story = generate_story(
                        "The Guard Room", "fight the ghostly knight", outcome, "You dodge the knight's sword. The armour crashes to the floor."
                    )
                    set_result("success", story)
                    st.rerun()
            with right:
                if st.button("🏃 Run past"):
                    outcome = "The player escapes past the knight without injury."
                    story = generate_story(
                        "The Guard Room", "running past the ghostly knight", outcome, "You sprint past the knight and escape through the doorway."
                    )
                    set_result("success", story)
                    st.rerun()
        else:
            show_result()
            show_continue_button()
 
 

    # ============================================================
    # ROOM 6 — DUNGEON (INVENTORY PERSISTS ACROSS ROOMS)
    # ============================================================
    elif room == "dungeon":
        show_room("Dungeon", "In a large room with lots of items, you see a healing potion.")
        if not st.session_state.action_complete:
                if "Healing Potion" in st.session_state.inventory:
                    st.info("You already have a healing potion.")
                    show_continue_button()
                else:
                    left, right = st.columns(2)
                    with left:
                        if st.button("🍷 Take the healing potion"):
                            add_item("Healing Potion")
                            outcome = "The player takes the Healing Potion."
                            story = generate_story(
                                "The Dungeon", "take the healing potion", outcome,
                                "You take the healing potion."
                            )
                            set_result("success", story)
                    with right:
                        if st.button("🌿Leave the healing potion behind"):
                            outcome = "The player leaves the healing potion behind."
                            story = generate_story(
                                "The Dungeon", "leave the healing potion behind", outcome,
                                "You leave the potion."
                            )
                            set_result("story", story)
        else:
            show_result()
            show_continue_button()
 
 
    #see a bottle of red liquid
    #left - take it, find a healing potion
    #right - leave it, leave the bottle behind
    
    # ============================================================
    # ROOM 7 — CASTLE GATE (BRANCH BASED ON INVENTORY)
    # ============================================================
    elif room == "castle_gate":
        show_room("The castle gate", "A towering iron gate, flanked by high stone walls, stands before you.")
        if "Iron Key"  in st.session_state.inventory:
            st.info("🗝️You are carrying an iron key.")
        if not st.session_state.action_complete:
            if "Iron Key" in st.session_state.inventory:
                if st.button("🚪 Open the castle gate"):
                    outcome = "The player unlocks the gate with the Iron Key and escapes the castle."
                    story = generate_story(
                        "The Castle Gate", "unlock the gate with the Iron Key", outcome,
                        "You unlock the gate with the Iron Key and escape the castle."
                    )
                    set_result("success", story)
                    st.balloons()
            else:
                st.warning("🔒 The gate is locked, You do not have the key." )
                if not st.session_state.action_complete:
                    chance_encounter(
                    "🧗 Climb the wall",
                    "The Castle Gate",
                    "climb over the ruined wall",
                    4,
                    "The player climbs over the ruinded wall and lands outside.",
                    "The player slips, loses 1 health, and does NOT escape",
                    "You slip and crash painfully against the stone wall.",
                    1)
        else:
            show_result()
            if st.session_state.result_type == "success":
                st.header("🏆 YOU ESCAPED THE CASTLE!")
                st.balloons()
            elif st.session_state.health > 0:
                    if st.button("🧗 Try Again"):
                        st.session_state.action_complete = False
                        st.session_state.result_type = ""
                        st.session_state.result_message = ""
                        st.session_state.result_value = ""
                        st.rerun()
    else:
        show_result()
        st.header("🏆 YOU ESCAPED THE CASTLE!")
        st.balloons()

    st.divider()
    if st.button("🔄 Play Again"):
        restart_game() 
