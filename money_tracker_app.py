import streamlit as st
import json
import os

FILENAME = "transactions.json"
YOUR_NAME = "Black Jacks"

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f)

# App
st.title("💰 Tejas Money Tracker")

transactions = load_data()

action = st.radio("Select Action", ["Give Money", "Receive Money", "Clear Dues"])

name = st.text_input("Person Name")
amount = st.number_input("Amount (Rs)", min_value=0, step=10)

if st.button("Submit"):
    if name:
        if action == "Give Money":
            transactions[name] = -abs(amount)
            st.success(f"Tejas will give {amount}Rs to {name}")
        elif action == "Receive Money":
            transactions[name] = abs(amount)
            st.success(f"Tejas will receive {amount}Rs from {name}")
        elif action == "Clear Dues":
            transactions[name] = 0
            st.info(f"Cleared dues with {name}")
        save_data(transactions)
    else:
        st.error("Please enter a name.")

# Summary
st.subheader("📋 Transaction Summary")
total = 0
for person, value in transactions.items():
    if value > 0:
        st.write(f"Tejas ← {person} [{value}Rs]")
    elif value < 0:
        st.write(f"Tejas → {person} [{-value}Rs]")
    else:
        st.write(f"Tejas → {person} [Nothing Pay]")
    total += value

st.markdown("---")
st.markdown(f"### 💼 Balance: `{total} Rs`")
