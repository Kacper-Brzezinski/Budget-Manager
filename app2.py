import json      # Import data from file
from datetime import datetime       # Import the current time
import sys   # Allows to use system functions

# Load data from a file in read mode and close the file correctly
def load_transactions(filename="data.json"):        
     with open(filename, "r") as file:
         return json.load(file)
     
# Main Function
def show_balance():
    transactions = load_transactions()  #Storing data in a variable

    # Get the current date and month
    now = datetime.now()
    current_year_month = now.strftime("%Y-%m")

    #Transaction filtering (current month)
    month_transactions = []
    for t in transactions :
        if t["timestamp"].startswith(current_year_month):
            month_transactions.append(t)

    # Separation of incomes and expenses
    incomes = []
    expenses = []
    for t in month_transactions:
        if t["type"] == "income":
            incomes.append(t)
        elif t["type"] == "expense":
            expenses.append(t)

    print(f"===== {now.strftime('%B %Y')} Account Summary =====")

    # Counting all incomes and expenses for the current month
    total_income = 0
    for t in incomes:
        total_income += t["amount"]
    print(f"Total income:   ${total_income:.2f}")

    total_expense = 0
    for t in expenses:
        total_expense += t["amount"]
    print(f"Total expense:  ${total_expense:.2f}")
    
    balance = total_income - total_expense
    print(f"-------------------------------")
    print(f"For: {now.strftime('%B %Y')} Current balance: ${balance:.2f}")

    print(f"-------------------------------")
    print(f"For: {now.strftime('%B %Y')} Transaction History:")
    
    # Counting the number of transactions
    income_count = len(incomes)
    expense_count = len(expenses)
    total_transactions = len(month_transactions)
    
    print(f"Income transactions: {income_count}")
    print(f"Expenses transactions: {expense_count}")
    print(f"Total transactions: {total_transactions}")
    
    print(f"===== {now.strftime('%B %Y')} Transactions =====")
    if total_transactions == 0:
        print(f"No transactions for this month.")
    else:
        for t in month_transactions:
            print(f"{t['timestamp']} | {t['type'].capitalize():8} | ${t['amount']:8.2f} | {t['category']:15} | {t['description']}")

    all_income = 0
    all_expense = 0
    
    for t in transactions:
        if t["type"] == "income":
            all_income += t["amount"]
        elif t["type"] == "expense":
            all_expense += t["amount"]
    overall_balance = all_income - all_expense



    print(f"\n===== Overall Account Balance =====")
    print(f"Total income:   ${all_income:.2f}")
    print(f"Total expense:  ${all_expense:.2f}")
    print(f"Overall balance: ${overall_balance:.2f}")

    # Displays the number of all transactions in the file
    all_incomes_count = 0
    all_expenses_count = 0
    
    for t in transactions:
     if t["type"] == "income":
        all_incomes_count += 1
     elif t["type"] == "expense":
        all_expenses_count += 1
     
    print(f"\nTotal number of incomes: {all_incomes_count}")
    print(f"Total number of expenses: {all_expenses_count}")
    print(f"Overall number of transactions: {len(transactions)}")

if __name__ == "__main__":
    # Check if the first argument is 'show_balance'
    if len(sys.argv) > 1 and sys.argv[1] == "show_balance":
        show_balance()
    else:
        print("Usage: python filename.py show_balance")

