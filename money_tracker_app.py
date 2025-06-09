import streamlit as st
import json
import os

# Predefined list
person_list = ["Tejas", "Kaki", "Gouda", "Pavan", "Agadi", "Gani", "Ravi", "Anil"]

st.title("💰 Personal Money Tracker App")

# --- Step 1: Select your name ---
your_name_display = st.selectbox("Select your name to start:", person_list)
your_name = your_name_display.strip().lower()
FILENAME = f"{your_name}.json"

# Load user's transaction file
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

# Save to user's transaction file
def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f)

# Reset file
def clear_all():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

transactions = load_data()

# --- Step 2: Actions ---
st.subheader(f"Welcome, {your_name_display}!")
action = st.radio("Choose an Action:", ["Give Money", "Receive Money", "Clear Dues", "Clear ALL"])

if action == "Clear ALL":
    if st.button("⚠️ Reset All Transactions"):
        clear_all()
        transactions = {}
        st.success("All transactions cleared! Start fresh.")
else:
    # List excluding self
    other_people = [p for p in person_list if p.lower() != your_name]
    selected_name_display = st.selectbox("Choose a person:", other_people)
    name = selected_name_display.strip().lower()
    amount = st.number_input("Enter amount (Rs):", min_value=0, step=10)

    if st.button("Submit Transaction"):
        if action == "Give Money":
            transactions[name] = -abs(amount)
            st.success(f"You gave {amount}Rs to {selected_name_display}")
        elif action == "Receive Money":
            transactions[name] = abs(amount)
            st.success(f"You received {amount}Rs from {selected_name_display}")
        elif action == "Clear Dues":
            transactions[name] = 0
            st.info(f"Cleared dues with {selected_name_display}")
        save_data(transactions)

# --- Step 3: Summary ---
if transactions:
    st.subheader("📋 Transaction Summary")
    total = 0
    for person, value in transactions.items():
        person_name = person.capitalize()
        if value > 0:
            st.write(f"{your_name_display} ← {person_name} [{value}Rs]")
        elif value < 0:
            st.write(f"{your_name_display} → {person_name} [{-value}Rs]")
        else:
            st.write(f"{your_name_display} → {person_name} [Nothing Pay]")
        total += value
    st.markdown("---")
    st.markdown(f"### 💼 Balance: `{total} Rs`")
else:
    st.info("No transactions yet. Start by adding one.")
