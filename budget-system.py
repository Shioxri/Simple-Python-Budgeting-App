import json
import os
from datetime import datetime

BUDGET_FILE = "budget.json"
HISTORY_FILE = "history.json"
DEPOSIT_FILE = "deposit.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def set_budget():
    budget = float(input("Enter your budget for the week: "))
    budget_data = {"budget": budget}
    save_data(BUDGET_FILE, budget_data)
    print(f"Budget set to {budget}")

def reset_budget():
    confirm = input("Are you sure you want to reset the budget? (y/n): ")
    if confirm.lower() == 'y':
        save_data(BUDGET_FILE, {"budget": 0})
        save_data(HISTORY_FILE, {"history": []})
        print("Budget and history reset.")

def subtract_money():
    amount = float(input("Enter the amount to subtract: "))
    description = input("Enter the description of the expense: ")
    budget_data = load_data(BUDGET_FILE)
    if budget_data["budget"] >= amount:
        budget_data["budget"] -= amount
        save_data(BUDGET_FILE, budget_data)
        history = load_data(HISTORY_FILE).get("history", [])
        history.append({"type": "subtract", "amount": amount, "description": description, "date": str(datetime.now())})
        save_data(HISTORY_FILE, {"history": history})
        print(f"Subtracted {amount} for {description}. Remaining budget: {budget_data['budget']}")
    else:
        print("Insufficient budget!")

def add_money():
    amount = float(input("Enter the amount to add: "))
    description = input("Enter the description of the addition: ")
    budget_data = load_data(BUDGET_FILE)
    budget_data["budget"] += amount
    save_data(BUDGET_FILE, budget_data)
    history = load_data(HISTORY_FILE).get("history", [])
    history.append({"type": "add", "amount": amount, "description": description, "date": str(datetime.now())})
    save_data(HISTORY_FILE, {"history": history})
    print(f"Added {amount} for {description}. Total budget: {budget_data['budget']}")

def deposit_money():
    budget_data = load_data(BUDGET_FILE)
    amount = budget_data["budget"]
    if amount > 0:
        deposits = load_data(DEPOSIT_FILE).get("deposits", [])
        deposits.append({"amount": amount, "date": str(datetime.now())})
        save_data(DEPOSIT_FILE, {"deposits": deposits})
        save_data(BUDGET_FILE, {"budget": 0})
        print(f"Deposited {amount}. Budget reset to 0.")
    else:
        print("No money to deposit.")

def view_history():
    budget_data = load_data(BUDGET_FILE)
    history = load_data(HISTORY_FILE).get("history", [])
    deposits = load_data(DEPOSIT_FILE).get("deposits", [])
    print("\n=========================================================\n")
    print(f"\nCurrent Budget: {budget_data.get('budget', 0)}")
    print("\nTransaction History:")
    for entry in history:
        print(f"{entry['date']}: {entry['type']} - {entry['description']} - ${entry['amount']}")

    print("\nDeposits:")
    for deposit in deposits:
        print(f"{deposit['date']}: ${deposit['amount']}")
    print("\n=========================================================\n")
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Set Budget")
        print("2. Reset Budget")
        print("3. Subtract money from budget")
        print("4. Add money to budget")
        print("5. Deposit Money")
        print("6. View History")
        print("7. Quit")

        choice = input("Choose an option: ")
        if choice == '1':
            set_budget()
        elif choice == '2':
            reset_budget()
        elif choice == '3':
            subtract_money()
        elif choice == '4':
            add_money()
        elif choice == '5':
            deposit_money()
        elif choice == '6':
            view_history()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
