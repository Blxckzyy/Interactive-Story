#py -m streamlit run app.py
import streamlit as st

# STEP 1 — Initialise game values once per browser session.
# Streamlit reruns the script when the player interacts with a widget.
# These values need to survive those reruns.
 
if "playerName" not in st.session_state:
    st.session_state.playerName = ""
if "health" not in st.session_state:
    st.session_state.health = 100
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "scene" not in st.session_state:
    st.session_state.scene = "start" 
if "result" not in st.session_state:
    st.session_state.result = ""


# STEP 2 — Show the game's title and the information the player carries.
 
st.title("Escape The Castle")

if st.session_state.playerName:
    st.write(f"Player: {st.session_state.playerName}")
    st.write(f"Health: {st.session_state.health}")
    st.write(f"Inventory: {st.session_state.inventory}")

# STEP 3 — Start screen: use a text input and button.
# The name is saved to session state so it is available in later scenes
if st.session_state.scene == "start":
    st.subheader("Create your character")
    st.session_state.playerName = st.text_input("What is your name? ")
    if st.button("Start Adventure"):
        playerName = st.session_state.playerName.strip()
        if not playerName:
            st.warning("Please enter your name before starting.")
        else:
            st.session_state.playerName = playerName
            st.session_state.scene = "cell"
            st.rerun()

# STEP 4 — Cell scene: convert the terminal choices into buttons.
# Store the result so it stays visible after other interactions.
elif st.session_state.scene == "cell":
    st.subheader("The Cell")
    st.write("You wake up in a dark cell.")
    st.write("You can see a door, a window, and an old bed")

    if st.button("Investigate the door"):
        st.session_state.result = "The door is locked, you need a key."
    if st.button("Investigate the window"):
        st.session_state.result = "The window isn't an option to escape, it is barred off."
    if st.button("Investigate the bed"):
        if "Iron Key" not in st.session_state.inventory:
            st.session_state.inventory.append("Iron Key")
            st.session_state.result = "You found an Iron Key!"
        else:
            st.session_state.result = "There is nothing else under the bed."
    if st.session_state.result:
            st.info(st.session_state.result)

# STEP 5 — Unlock progress using a condition based on inventory.
    if "Iron Key" in st.session_state.inventory:
        if st.button("Unlock the door and continue"):
            st.session_state.scene = "corridor"
            st.session_state.result = ""
            st.rerun()

# STEP 6 — Corridor scene: use the SAME inventory as in the Cell.
#Initialise the corridor scene - they player needs to notice a cabinet
elif st.session_state.scene == "corridor":
    st.subheader("The Corridor")
    st.write("As you walk out of the cell and into the corridor, you see an old warped and rotted cabinet ")
    if st.button("Look inside of the cabinet"):
        if "Rusty Dagger" not in st.session_state.inventory:
            st.session_state.inventory.append("Rusty Dagger")
            st.session_state.result = "You found a Rusty Dagger!"
        else:
            st.session_state.result = "There is nothing else in the cabinet."

    if st.session_state.result not in (
        "You found a Rusty Dagger!",
        "There is nothing else in the cabinet.",
    ):
        if st.button("Don't look inside the cabinet"):
            st.session_state.scene = "encounter"
            st.session_state.result = "You continue down the corridor, ignoring the cabinet."
            st.rerun()
    
    if st.session_state.result:
        st.info(st.session_state.result)

    if st.session_state.result in ("You found a Rusty Dagger!", "There is nothing else in the cabinet.",):
        if st.button("Continue down the corridor"):
            st.session_state.scene = "encounter"
            st.session_state.result = "You continue down the corridor, putting the Rusty Dagger in your pocket."
            st.rerun()

elif st.session_state.scene == "encounter":
    st.info(st.session_state.result)