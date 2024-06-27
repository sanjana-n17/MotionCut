import csv
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self, data_file, category_file, currency_file):
        self.data_file = data_file
        self.category_file = category_file
        self.currency_file = currency_file
        self.expenses = []
        self.categories = []
        self.currency = self.load_or_set_currency()
        self.load_data()
        self.load_categories()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]
    
    def save_data(self):
        with open(self.data_file, 'w', newline='') as file:
            fieldnames = ['amount', 'description', 'category', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)
    
    def load_categories(self):
        if os.path.exists(self.category_file):
            with open(self.category_file, 'r') as file:
                reader = csv.reader(file)
                self.categories = [row[0] for row in reader]
        else:
            self.setup_categories()
    
    def save_categories(self):
        with open(self.category_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for category in self.categories:
                writer.writerow([category])
    
    def setup_categories(self):
        print("Please set up your expense categories :)")
        while True:
            category = input("Enter a category (or type 'done' to finish): ").strip()
            if category.lower() == 'done':
                break
            elif category and category.lower() not in [cat.lower() for cat in self.categories]:
                self.categories.append(category)
        self.save_categories()
    
    def load_or_set_currency(self):
        if os.path.exists(self.currency_file):
            with open(self.currency_file, 'r') as file:
                return file.read().strip()
        else:
            return self.set_currency()
    
    def save_currency(self):
        with open(self.currency_file, 'w') as file:
            file.write(self.currency)
    
    def set_currency(self):
        print("Please set the currency type (e.g., USD, EUR, GBP).")
        currency = input("Enter currency: ").strip().upper()
        if currency:
            self.currency = currency
            self.save_currency()
            return currency
        else:
            print("Invalid input. Using default currency (USD).")
            self.currency = "USD"
            self.save_currency()
            return "USD"
    
    def add_expense(self, amount, category, description="", date=None):
        if not self.categories:
            print("No categories available. Please set up categories first.")
            return
        
        if category.lower() not in [cat.lower() for cat in self.categories]:
            print(f"Category '{category}' not found. Please add it to your categories first.")
            return

        if date is None:
            date = datetime.now().strftime('%d-%m-%Y')
        else:
            try:
                datetime.strptime(date, '%d-%m-%Y')
            except ValueError:
                print("Invalid date.")
                return

        expense = {
            'amount': amount,
            'description': description,
            'category': category,
            'date': date
        }
        self.expenses.append(expense)
        self.save_data()
    
    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_data()
            print("Expense deleted successfully.")
        else:
            print("Invalid index. Please try again.")
    
    def get_summary(self, start_date=None, end_date=None):
        if not self.expenses:
            print("No entries found.")
            return
        
        filtered_expenses = self.expenses
        if start_date and end_date:
            filtered_expenses = [
                expense for expense in self.expenses
                if 'date' in expense and start_date <= datetime.strptime(expense['date'], '%d-%m-%Y') <= end_date
            ]

        total_expense = sum(float(expense['amount']) for expense in filtered_expenses)
        
        if not filtered_expenses:
            print("No entries found in the specified period.")
            return
        
        category_summary = {}

        for expense in filtered_expenses:
            category = expense['category']
            amount = float(expense['amount'])
            if category in category_summary:
                category_summary[category] += amount
            else:
                category_summary[category] = amount

        print(f"Total Expense: {self.currency} {total_expense:.2f}")
        print("Category-wise Breakdown:")
        for category, amount in category_summary.items():
            print(f"  {category}: {self.currency} {amount:.2f}")

    def get_monthly_summary(self, year, month):
        if not self.expenses:
            print("No entries found.")
            return
        
        try:
            start_date = datetime.strptime(f'01-{month:02d}-{year}', '%d-%m-%Y')
            if month == 12:
                end_date = datetime.strptime(f'01-01-{year + 1}', '%d-%m-%Y')
            else:
                end_date = datetime.strptime(f'01-{month + 1:02d}-{year}', '%d-%m-%Y')
            self.get_summary(start_date, end_date)
        except ValueError:
            print("Invalid month or year. Please enter a valid month (1-12) and a valid year.")

    def get_yearly_summary(self, year):
        if not self.expenses:
            print("No entries found.")
            return
        
        try:
            start_date = datetime.strptime(f'01-01-{year}', '%d-%m-%Y')
            end_date = datetime.strptime(f'01-01-{year + 1}', '%d-%m-%Y')
            self.get_summary(start_date, end_date)
        except ValueError:
            print("Invalid year. Please enter a valid year.")

    def get_custom_summary(self):
        if not self.expenses:
            print("No entries found.")
            return
        
        while True:
            start_date_str = input("Enter start date (DD-MM-YYYY): ")
            end_date_str = input("Enter end date (DD-MM-YYYY): ")
            try:
                start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
                end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
                if start_date > end_date:
                    print("Start date cannot be after end date. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        
        self.get_summary(start_date, end_date)

    def manage_categories(self):
        while True:
            print("1. Add Category")
            print("2. Remove Category")
            print("3. View Categories")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.setup_categories()
            elif choice == '2':
                if not self.categories:
                    print("No categories available to remove.")
                else:
                    print("Current Categories:")
                    for idx, category in enumerate(self.categories, start=1):
                        print(f"{idx}. {category}")
                    try:
                        category_choice = int(input("Enter the index of the category to remove: "))
                        if 1 <= category_choice <= len(self.categories):
                            removed_category = self.categories.pop(category_choice - 1)
                            self.save_categories()
                            print(f"Category '{removed_category}' removed successfully.")
                        else:
                            print("Invalid category index.")
                    except ValueError:
                        print("Invalid input. Please enter a valid index number.")
            elif choice == '3':
                if not self.categories:
                    print("No categories available.")
                else:
                    print("Current Categories:")
                    for category in self.categories:
                        print(f"  - {category}")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    tracker = ExpenseTracker('expenses.csv', 'categories.csv', 'currency.txt')

    while True:
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. View Summary")
        print("4. Manage Categories")
        print("5. Set Currency")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                if not tracker.categories:
                    print("No categories available. Please set up categories first.")
                else:
                    amount = float(input(f"Enter amount ({tracker.currency}): "))
                    print("Select a category from the following:")
                    for idx, category in enumerate(tracker.categories, start=1):
                        print(f"{idx}. {category}")
                    category_choice = int(input("Enter category number: "))
                    if 1 <= category_choice <= len(tracker.categories):
                        category = tracker.categories[category_choice - 1]
                        description_choice = input("Do you want to add a description? (yes/no): ").strip().lower()
                        description = ""
                        if description_choice == 'yes':
                            description = input("Enter description: ")
                        date = input("Enter date (DD-MM-YYYY) or press Enter for today: ").strip()
                        if date == "":
                            date = None
                        tracker.add_expense(amount, category, description, date)
                    else:
                        print("Invalid category choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number for amount.")
        elif choice == '2':
            try:
                if not tracker.expenses:
                    print("No expenses available to delete.")
                else:
                    print("Current Expenses:")
                    for idx, expense in enumerate(tracker.expenses, start=1):
                        print(f"{idx}. {expense['amount']} {tracker.currency} spent on {expense['category']} ({expense['date']})")
                    expense_choice = int(input("Enter the index of the expense to delete: "))
                    if 1 <= expense_choice <= len(tracker.expenses):
                        tracker.delete_expense(expense_choice - 1)
                    else:
                        print("Invalid expense index.")
            except ValueError:
                print("Invalid input. Please enter a valid index number.")
        elif choice == '3':
            print("1. Monthly Summary")
            print("2. Yearly Summary")
            print("3. Custom Date Range Summary")
            summary_choice = input("Enter your choice: ")

            if summary_choice == '1':
                try:
                    year = int(input("Enter year (YYYY): "))
                    month = int(input("Enter month (MM): "))
                    if 1 <= month <= 12:
                        tracker.get_monthly_summary(year, month)
                    else:
                        print("Invalid month. Please enter a value between 1 and 12.")
                except ValueError:
                    print("Invalid input. Please enter valid numbers for year and month.")
            elif summary_choice == '2':
                try:
                    year = int(input("Enter year (YYYY): "))
                    tracker.get_yearly_summary(year)
                except ValueError:
                    print("Invalid input. Please enter a valid year.")
            elif summary_choice == '3':
                tracker.get_custom_summary()
            else:
                print("Invalid choice.")
        elif choice == '4':
            tracker.manage_categories()
        elif choice == '5':
            tracker.set_currency()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
