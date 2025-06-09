import streamlit as st
import json
import os

st.title("💰 Personal Money Tracker App")

# --- Step 1: Enter your name ---
your_name = st.text_input("Enter your name to start:", value="")

if your_name:
    FILENAME = f"{your_name.lower()}.json"

    # Load your own data
    def load_data():
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                return json.load(f)
        return {}

    def save_data(data):
        with open(FILENAME, "w") as f:
            json.dump(data, f)

    transactions = load_data()

    # Step 2: Actions
    action = st.radio("Select Action", ["Give Money", "Receive Money", "Clear Dues"])
    name = st.text_input("Person Name")
    amount = st.number_input("Amount (Rs)", min_value=0, step=10)

    if st.button("Submit"):
        if name:
            if action == "Give Money":
                transactions[name] = -abs(amount)
                st.success(f"You gave {amount}Rs to {name}")
            elif action == "Receive Money":
                transactions[name] = abs(amount)
                st.success(f"You received {amount}Rs from {name}")
            elif action == "Clear Dues":
                transactions[name] = 0
                st.info(f"Cleared dues with {name}")
            save_data(transactions)
        else:
            st.error("Please enter a person's name.")

    # Step 3: Summary
    st.subheader("📋 Transaction Summary")
    total = 0
    for person, value in transactions.items():
        if value > 0:
            st.write(f"{your_name} ← {person} [{value}Rs]")
        elif value < 0:
            st.write(f"{your_name} → {person} [{-value}Rs]")
        else:
            st.write(f"{your_name} → {person} [Nothing Pay]")
        total += value

    st.markdown("---")
    st.markdown(f"### 💼 Balance: `{total} Rs`")

else:
    st.info("Please enter your name to get started.")
