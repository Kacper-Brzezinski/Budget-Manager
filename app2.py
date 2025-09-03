import json  # Import data from file
from datetime import datetime  # Import the current time
import sys  # Allows to use system functions

# Changing the month names to numbers
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

    # Date range for filtering
    current_year = now.year

    # Month range
    if month:
        # If month is a month name (APRIL, April, april)
        if len(month) > 2 and not month.isdigit():
            month_num = month_name_to_number(month)
            if not month_num:
                print("Bad name of month!")
                return
            filter_month = month_num
            # If month is a number
        elif len(month) == 2 and month.isdigit():
            filter_month = month
             # If month is YYYY-MM format
        elif len(month) == 7 and month[4] == "-":
            filter_month = month[5:7]
        else:
            print("Incorrect month format!")
            return
    # Else month=NONE
    else:
        filter_month = None

    # Transaction filtering function
    '''Function that filters transactions based on year, month, and category. 
    It iterates through the transactions and adds those that meet the conditions to the filtered list.'''
    def filter_transactions(transactions, year=None, month=None, category=None):
        filtered = []
        for t in transactions:
            t_date = t["timestamp"]
            t_year = int(t_date[:4])
            t_month = t_date[5:7]
            if year and t_year != year:  # Check if year is not a transaction year
                continue
            if month and t_month != month:  # Check if month is not a transaction month
                continue
            if category and t["category"].lower() != category.lower():  # Check if category is not a category transaction
                continue
            filtered.append(t) # adds the transaction to the filtered list if it meets all the conditions
        return filtered  # returns a list of filtered transactions

    # Filter transactions based on the given parameters
    filtered_transactions = transactions

    if month:  #checks if the argument month has been provided
        # filters transactions based on year and month
        filtered_transactions = filter_transactions(filtered_transactions, year=current_year, month=filter_month)
    if category: # checks if a category has been provided
        # filters transactions based on year and category
        filtered_transactions = filter_transactions(filtered_transactions, year=current_year, category=category)

    # Variables to store the sum of incomes, expenses sets initial states to 0
    total_income_month = 0
    total_expense_month = 0
    income_count_month = 0
    expense_count_month = 0

    # History transactions in month
    month_transactions = []
    
    '''It iterates through all transactions and filters them based on the month and category. 
    It adds transactions to the month_transactions list and counts the totals of revenues and expenses.'''
    
    for t in transactions:
        t_date = t["timestamp"]
        t_year = int(t_date[:4]) # converts the first part of the date to the year
        t_month = t_date[5:7]  # gets the month number from the date
        # Checking if the transaction falls within the selected month
        if month: # checks if the argument month has been provided
            if t_year != current_year or t_month != filter_month:  # checks if the year or the month number of the transaction is not equal to the given one
                continue
        # If category is provided also filter by it
        if category: # checks if a category has been provided
            if t["category"].lower() != category.lower(): #checks if the transaction category is not equal to the given category (ignoring case sensitivity)
                continue
        # Add the list of month transaction
        if (not month) or (t_year == current_year and t_month == filter_month): # checks if the transaction falls within the selected month
            month_transactions.append(t)

        # Count the incomes and expenses of the month
        if t["type"] == "income":
            total_income_month += t["amount"]
            income_count_month += 1
        elif t["type"] == "expense":
            total_expense_month += t["amount"]
            expense_count_month += 1

    # Display summaries
    if month: # checks if the argument month has been provided
        # Header for the month
        if len(month) > 2 and not month.isdigit():  # If month is month name
            display_month = month.capitalize() # converts the name of the month to uppercase
        elif len(month) == 2 and month.isdigit(): # if month is month number
            months_list = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            display_month = months_list[int(filter_month)-1] # gets the name of the month from the list
        elif len(month) == 7 and month[4] == "-":       # if month is format YYYY-MM
            display_month = datetime.strptime(month[:7], "%Y-%m").strftime("%B") # converts the format YYYY-MM to the name of the month
        else:
            display_month = now.strftime("%B") # gets the current month name
        display_year = current_year # sets the year to the current year
         
        # Display for the month
        print(f"===== {display_month} {display_year} =====")
        print(f"Incomes: ${total_income_month:.2f}")
        print(f"Expenses:  ${total_expense_month:.2f}")
        print(f"Balance:   ${total_income_month - total_expense_month:.2f}")
        print(f"Transactions: {income_count_month} incomes, {expense_count_month} expenses")
        print(f"\nHistory of transactions in {display_month} {display_year}:")
        if not month_transactions:
            print("No transactions in this month")
        else:
            for t in month_transactions:
                print(f"{t['timestamp']} | {t['type'].capitalize():8} | ${t['amount']:8.2f} | {t['category']:15} | {t['description']}")
    elif category:
        # Summaries for Category
        print(f"===== Category summary '{category}' in the year {current_year} =====")
        print(f"Incomes: ${total_income_month:.2f}")
        print(f"Expenses:  ${total_expense_month:.2f}")
        print(f"Balance:   ${total_income_month - total_expense_month:.2f}")
        print(f"Transactions: {income_count_month} incomes, {expense_count_month} expenses")
        
        # Display transaction details for the category in the year
        print(f"\nCategory transaction details '{category}' in the year {current_year}:")
        for t in transactions:
            t_date = t["timestamp"] # retrieves the transaction date from the timestamp field
            t_year = int(t_date[:4]) # converts the first part of the date to the year
            if t_year != current_year: # checks if the transaction year is not equal to the current year
                continue
            if t["category"].lower() != category.lower(): # checks if the transaction category is not equal to the given category (ignoring case sensitivity)
                continue
            print(f"{t['timestamp']} | {t['type'].capitalize():8} | ${t['amount']:8.2f} | {t['category']:15} | {t['description']}")
    else:
        # No month and category: only year summary
        print(f"===== Summary of the year {current_year} =====")
        print(f"Incomes: ${total_income_month:.2f}")
        print(f"Expenses:  ${total_expense_month:.2f}")
        print(f"Balance:   ${total_income_month - total_expense_month:.2f}")
        print(f"Transactions: {income_count_month} incomes, {expense_count_month} expenses")

if __name__ == "__main__":
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
        print("Usage: python filename.py show_balance [month=] [category=]")



