import streamlit as st
import json
import os

st.title("💰 Personal Money Tracker App")

# --- Step 1: Get user's name ---
your_name = st.text_input("Enter your name to start:", value="").strip().lower()

if your_name:
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
    st.subheader(f"Welcome, {your_name.capitalize()}!")
    action = st.radio("Choose an Action:", ["Give Money", "Receive Money", "Clear Dues", "Clear ALL"])

    if action == "Clear ALL":
        if st.button("⚠️ Reset All Transactions"):
            clear_all()
            transactions = {}
            st.success("All transactions cleared! Start fresh.")
    else:
        name = st.text_input("Enter other person's name:").strip().lower()
        amount = st.number_input("Enter amount (Rs):", min_value=0, step=10)

        if st.button("Submit Transaction"):
            if not name:
                st.warning("Please enter a valid name.")
            else:
                if action == "Give Money":
                    transactions[name] = -abs(amount)
                    st.success(f"You gave {amount}Rs to {name.capitalize()}")
                elif action == "Receive Money":
                    transactions[name] = abs(amount)
                    st.success(f"You received {amount}Rs from {name.capitalize()}")
                elif action == "Clear Dues":
                    transactions[name] = 0
                    st.info(f"Cleared dues with {name.capitalize()}")
                save_data(transactions)

    # --- Step 3: Summary ---
    if transactions:
        st.subheader("📋 Transaction Summary")
        total = 0
        for person, value in transactions.items():
            person_name = person.capitalize()
            if value > 0:
                st.write(f"{your_name.capitalize()} ← {person_name} [{value}Rs]")
            elif value < 0:
                st.write(f"{your_name.capitalize()} → {person_name} [{-value}Rs]")
            else:
                st.write(f"{your_name.capitalize()} → {person_name} [Nothing Pay]")
            total += value
        st.markdown("---")
        st.markdown(f"### 💼 Balance: `{total} Rs`")
    else:
        st.info("No transactions yet. Start by adding one.")
else:
    st.info("Enter your name above to begin tracking.")
