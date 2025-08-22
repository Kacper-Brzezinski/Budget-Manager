"""
PLAN KODU:
1. import danych z pliku data.json
2. import czasu aktualnego
3. Załadowanie danych z pliku do zmiennej dzięki funkcji
4. Zapisanie danych w zmiennej
5. Zmiana formatu daty na YYYY-MM-DD-T
6. Filtrowanie transakcji na aktualny miesiąc 
7. Wykazanie i odseparowanie wydatków i przychodów w aktualnym miesiącu 
8. Zliczanie całego przychodu i wydatku w akutalnym miesiącu 
9. Zliczanie transakcji 
10. Wyświetlenie wyników dla aktualnego miesiąca
11. Wyświetlanie i zliczanie aktualnego budżetu konta ogólnego
12. Wywołanie funkcji show_balance()

"""


import json
from datetime import datetime
import sys

def load_transactions(filename="data.json"):
    with open(filename, "r") as file:
        return json.load(file)

def show_balance():
    transactions = load_transactions()

    now = datetime.now()
    current_year_month = now.strftime("%Y-%m")

    month_transactions = []
    for t in transactions:
        if t["timestamp"].startswith(current_year_month):
            month_transactions.append(t)

    incomes = []
    expenses = []
    for t in month_transactions:
        if t["type"] == "income":
            incomes.append(t)
        elif t["type"] == "expense":
            expenses.append(t)

    total_income = 0
    for t in incomes:
        total_income += t["amount"]

    total_expense = 0
    for t in expenses:
        total_expense += t["amount"]

    balance = total_income - total_expense

    income_count = len(incomes)
    expense_count = len(expenses)
    total_transactions = len(month_transactions)

    print(f"===== {now.strftime('%B %Y')} Account Summary =====")
    print(f"Total income:   ${total_income:.2f} ({income_count} transactions)")
    print(f"Total expenses: ${total_expense:.2f} ({expense_count} transactions)")
    print("--------------------------")
    print(f"Current balance for {now.strftime('%B %Y')}: ${balance:.2f}")
    print(f"Total transactions: {total_transactions}\n")

    print(f"===== {now.strftime('%B %Y')} Transactions =====")
    if total_transactions == 0:
        print("No transactions for this month.")
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

    print("\n===== Overall Account Balance =====")
    print(f"Total income:   ${all_income:.2f}")
    print(f"Total expenses: ${all_expense:.2f}")
    print(f"Overall balance: ${overall_balance:.2f}")

if __name__ == "__main__":
    # Sprawdź, czy pierwszy argument to 'show_balance'
    if len(sys.argv) > 1 and sys.argv[1] == "show_balance":
        show_balance()
    else:
        print("Użycie: python nazwa_pliku.py show_balance")

    


   
