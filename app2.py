import json      # Import data from file
from datetime import datetime       # Import the current time
import sys   # Allows to use system functions

# Change month name to a number
def month_name_to_number(month_name):
    months = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12"
    }
    return months.get(month_name.lower())

# Load data from a file in read mode and close the file correctly
def load_transactions(filename="data.json"):        
     with open(filename, "r") as file:
         return json.load(file)
     
# Main Function
def show_balance(month=None, category=None):
    transactions = load_transactions()  #Storing data in a variable

    # Get the current date and month
    now = datetime.now()
    # Handling the month parameter (can be a name, number, or YYYY-MM)
    if month:
        # If month is the name of the month  (April, april, APRIL)
        if len(month) > 2 and not month.isdigit():  #Identifies whether the user entered the month name instead of the number or full format
            month_number = month_name_to_number(month)
            if not month_number:
                print("Bad name of month!")
                return
            current_year_month = f"{now.year}-{month_number}" #Connects the year with the month number
        # If month is the number of the month (04)
        elif len(month) == 2 and month.isdigit():
            current_year_month = f"{now.year}-{month}" #Connects the year with the month
        # If month is in the format YYYY-MM
        elif len(month) == 7 and month[4] == "-": 
            current_year_month = month
        else:
            print("Incorrect month format!")
            return
    else:
        current_year_month = now.strftime("%Y-%m")

    # Filtering transactions by month and category (ignoring case sensitivity)
    month_transactions = []
    for t in transactions:
        if t["timestamp"].startswith(current_year_month):
            if category:
                if t["category"].lower() == category.lower():
                    month_transactions.append(t)
            else:
                month_transactions.append(t)

    # Separation of incomes and expenses
    incomes = []
    expenses = []
    for t in month_transactions:
        if t["type"] == "income":
            incomes.append(t)
        elif t["type"] == "expense":
            expenses.append(t)

    # Set the name and year of the selected month to display in the header.
    if month:
    # If month is the name of the month (e.g. April, april, APRIL)
     if len(month) > 2 and not month.isdigit():
        display_month = month.capitalize()
        display_year = now.year
    # If month is the number of the month 
     elif len(month) == 2 and month.isdigit():
        months_list = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        display_month = months_list[int(month)-1]
        display_year = now.year
    # If month is in the format YYYY-MM
     elif len(month) == 7 and month[4] == "-":
        display_year = int(month[:4])
        month_number = int(month[5:7])
        months_list = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        display_month = months_list[month_number-1]
     else:
        display_month = now.strftime('%B')
        display_year = now.year
    else:
     display_month = now.strftime('%B')
     display_year = now.year

    print(f"===== {display_month} {display_year} Account Summary =====")


    # Counting all incomes and expenses for the filtered data
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
    print(f"For: {display_month} {display_year} Current balance: ${balance:.2f}")

    print(f"-------------------------------")
    print(f"For: {display_month} {display_year} Transaction History:")

    
    # Counting the number of transactions
    income_count = len(incomes)
    expense_count = len(expenses)
    total_transactions = len(month_transactions)
    
    print(f"Income transactions: {income_count}")
    print(f"Expenses transactions: {expense_count}")
    print(f"Total transactions: {total_transactions}")
    
    print(f"===== {display_month} {display_year} Transactions =====")
    if total_transactions == 0:
        print(f"No transactions for this month.")
    else:
        for t in month_transactions:
            print(f"{t['timestamp']} | {t['type'].capitalize():8} | ${t['amount']:8.2f} | {t['category']:15} | {t['description']}")

    # Summary only for filtered data
    all_income = 0
    all_expense = 0
    
    for t in month_transactions:
        if t["type"] == "income":
            all_income += t["amount"]
        elif t["type"] == "expense":
            all_expense += t["amount"]
    overall_balance = all_income - all_expense

    print(f"\n===== Overall Account Balance =====")
    print(f"Total income:   ${all_income:.2f}")
    print(f"Total expense:  ${all_expense:.2f}")
    print(f"Overall balance: ${overall_balance:.2f}")

    # Displays the number of all transactions in the filtered data
    all_incomes_count = 0
    all_expenses_count = 0
    
    for t in month_transactions:
        if t["type"] == "income":
            all_incomes_count += 1
        elif t["type"] == "expense":
            all_expenses_count += 1
     
    print(f"\nTotal number of incomes: {all_incomes_count}")
    print(f"Total number of expenses: {all_expenses_count}")
    print(f"Overall number of transactions: {len(month_transactions)}")

if __name__ == "__main__":
    # Argument handling: show_balance [month=...] [category=...]
    if len(sys.argv) > 1 and sys.argv[1] == "show_balance":
        month = None
        category = None
        for arg in sys.argv[2:]:
            if arg.lower().startswith("month="):
                month = arg.split("=", 1)[1]
            elif arg.lower().startswith("category="):
                category = arg.split("=", 1)[1]
        show_balance(month=month, category=category)
    else:
        print("Usage: python filename.py show_balance [month=april] [category=rent]")

