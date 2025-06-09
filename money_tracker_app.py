import streamlit as st
import json
import os

# Predefined users
person_list = ["Teja", "Kaki", "Gouda", "Pavan", "Agadi", "Ganesh", "Ravi", "Anil"]

st.title("💰 Personal Money Tracker App")

# Step 1: Choose your name
your_name_display = st.selectbox("Select your name to start:", person_list)
your_name = your_name_display.strip().lower()
your_file = f"{your_name}.json"

# Helper functions
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def clear_all(file):
    if os.path.exists(file):
        os.remove(file)

# Load your data
transactions = load_data(your_file)

# Step 2: Choose action
st.subheader(f"Welcome, {your_name_display}!")
action = st.radio("Choose an Action:", ["Give Money", "Receive Money", "Clear Dues", "Clear ALL"])

if action == "Clear ALL":
    if st.button("⚠️ Reset All Transactions"):
        clear_all(your_file)
        transactions = {}
        st.success("All transactions cleared! Start fresh.")
else:
    # Select other person
    other_people = [p for p in person_list if p.lower() != your_name]
    selected_name_display = st.selectbox("Choose a person:", other_people)
    other_name = selected_name_display.strip().lower()
    other_file = f"{other_name}.json"

    amount = st.number_input("Enter amount (Rs):", min_value=0, step=10)

    if st.button("Submit Transaction"):
        # Load both user data
        transactions = load_data(your_file)
        other_transactions = load_data(other_file)

        if action == "Give Money":
            # Update giver
            transactions[other_name] = transactions.get(other_name, 0) - amount
            # Update receiver
            other_transactions[your_name] = other_transactions.get(your_name, 0) + amount
            st.success(f"You gave {amount}Rs to {selected_name_display}")
        elif action == "Receive Money":
            # Update receiver
            transactions[other_name] = transactions.get(other_name, 0) + amount
            # Update giver
            other_transactions[your_name] = other_transactions.get(your_name, 0) - amount
            st.success(f"You received {amount}Rs from {selected_name_display}")
        elif action == "Clear Dues":
            transactions[other_name] = 0
            other_transactions[your_name] = 0
            st.info(f"Cleared dues with {selected_name_display}")

        # Save updated files
        save_data(your_file, transactions)
        save_data(other_file, other_transactions)

# Step 3: Show summary
transactions = load_data(your_file)
if transactions:
    st.subheader("📋 Transaction Summary")
    total = 0
    for person, value in transactions.items():
        display_name = person.capitalize()
        if value > 0:
            st.write(f"{your_name_display} ← {display_name} [{value}Rs]")
        elif value < 0:
            st.write(f"{your_name_display} → {display_name} [{-value}Rs]")
        else:
            st.write(f"{your_name_display} → {display_name} [Nothing Pay]")
        total += value
    st.markdown("---")
    st.markdown(f"### 💼 Balance: `{total} Rs`")
else:
    st.info("No transactions yet. Start by adding one.")
