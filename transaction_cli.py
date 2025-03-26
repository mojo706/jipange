from transaction_manager import TransactionManager
from datetime import datetime

class TransactionCLI:
    def __init__(self):
        """Initialize the transaction CLI."""
        self.transaction_manager = TransactionManager()

    def display_menu(self):
        """Display the main menu options."""
        print("\n===== Personal Finance Manager =====")
        print("1. Transactions")
        print("2. Categories")
        print("3. Reports")
        print("4. Exit")
        return input("Enter your choice (1-4): ")
    
    def display_transaction_menu(self):
        """Display the transaction menu options."""
        print("\n----- Jipange -----")
        print("1. Add new transaction")
        print("2. View all transactions")
        print("3. Search transactions")
        print("4. Edit transactions")
        print("5. Delete transaction")
        print("6. Back to main menu")
        return input("Enter your choice (1-6): ")
    
    def display_category_menu(self):
        """Display the category menu options."""
        print("\n----- Category Management -----")
        print("1. View all categories")
        print("2. Add new category")
        print("3. Edit category")
        print("4. Delete category")
        print("5. Back to main menu")
        return input("Enter your choice (1-5): ")
    
    def display_report_menu(self):
        """Display the report menu options."""
        print("n----- Financial Reports -----")
        print("1. Income vs Expenses Summary")
        print("2. Category Breakdown")
        print("3. Back to main menu")
        return input("Enter your choice (1-3): ")
    
    def add_transaction_menu(self):
        """Menu for adding a new transaction."""
        print("\n----- Add New Transaction -----")

        #Get transaction details from user
        date_input = input("Date (YYYY-MM-DD) [today]: ")
        if not date_input:
            date_input = datetime.now().strftime("%Y-%m-%\d")


        # Transaction tyoe
        print("\nTransaction Type: ")
        print("1. Income")
        print("2. Expense")
        type_choice = input("Emter choice (1-2): ")
        transaction_type = "income" if type_choice == "1" else "expense"

        amount_input = input("Amount: ")

        # Show appropriate categories based on transaction type
        categories = self.transaction_manager.category_manager.get_categories(transaction_type)
        print("\nAvailable Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category['name']}")
        print(f"{len(categories) +1}. Add new category")

        category_choice = input(f"Select category (1-{len(categories) + 1}): ")

        if category_choice == str(len(categories) +1):
            
            new_category = input("Enter new category name: ")
            self.transaction_manager.category_manager.add_category(new_category, transaction_type)
            category = new_category
        else:
            try:
                category = categories[int(category_choice) -1]['name']
            except (ValueError, IndexError):
                print("Invalid selection. Using 'Miscellaneous'.")
                category = "Miscellaneous"

        
        account = input("Account (e.g., Cash, Checking, Credit Card): ")

        
        description = input("Description: ")

        
        success, message = self.transaction_manager.add_transaction(date_input, amount_input, category, account, description, transaction_type)

        if success:
            print("Transaction added Successfully")
        else:
            print(f"Error: {message}")
    
    def view_transactions(self):
        """View all transactions with simple filtering options."""
        print("\n----- Transaction History -----")

        print("Filter options (leave blank for all):")
        transaction_type = input("Type (income/expense): ")

        filters = {}
        if transaction_type:
            filters['transaction_type'] = transaction_type

        transactions = self.transaction_manager.get_transactions(filters)

        if not transactions:
            print("\nNo transactions found.")
            return
        
        self.display_transactions(transactions)

    def display_transactions(self, transactions):
        """Display a list of transactions in a formated table."""
        print(f"\nFound {len(transactions)} transactions.")
        print(f"\n{'ID':<10} {'Date':<12} {'Type':<8} {'Amount':<10} {'Category':<15} {'Account':<15} {'Description':<30}")
        print("-" * 100)

        for t in transactions:
            amount_str = f"${float(t['amount']):.2f}"
            print(f"{t['id'][:8]:<10} {t['date']:<12} {t['transaction_type']:<8} "
                  f"{amount_str:<10} {t['category'][:15]:<15} {t['account'][:15]:<15} {t['description'][:30]:<30}")
    
    def search_transactions_menu(self):
        """Menu for searching transactions."""
        print("\n----- Search Transactions -----")
        keyword = input("Enter search term: ")

        if not keyword:
            print("Search term cannot be empty.")
            return
        
        results = self.transaction_manager.search_transactions(keyword)

        if not results:
            print("No transactions found matching your search.")
            return
        
        self.display_transactions(results)

    def edit_transaction_menu(self):
        """Menu for editing a transaction."""
        print("\n----- Edit Transaction -----")
        transaction_id = input("Enter transaction ID to edit: ")

        
        transactions = self.transaction_manager.get_transactions({"id": transaction_id})

        if not transactions:
            print("Transaction not found.")
            return
        
        print("\nCurrent transaction details:")
        self.display_transactions(transactions)

        print("\nWhich field would you like to edit?")
        print("1. Date")
        print("2. Amount")
        print("3. Category")
        print("4. Account")
        print("5. Description")
        print("6. Transaction Type")

        field_choice = input("Enter choice (1-6): ")

        field_mapping = {
            "1": "date",
            "2": "amount",
            "3": "category",
            "4": "account",
            "5": "description",
            "6": "transaction_type"
        }

        if field_choice not in field_mapping:
            print("Invalid choice.")
            return
        
        field = field_mapping[field_choice]

        # Special handling for transaction type and category
        if field == "transaction_type":
            print("1. Income")
            print("2. Expense")
            type_choice = input("Enter choice (1-2): ")
            new_value = "income" if type_choice == "1" else "expense"
        elif field == "category":
            current_type = transactions[0]['transaction_type']

            categories = self.transaction_manager.category_manager.get_categories(current_type)
            print("\nAvailable Categories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category['name']}")
            print(f"{len(categories) +1}. Add new category")

            category_choice = input(f"Select category (1-{len(categories) +1}): ")

            if category_choice == str(len(categories) +1):
                new_value = input("Enter new category name: ")
                self.transaction_manager.category_manager.add_category(new_value, current_type)
            else:
                try:
                    new_value = categories[int(category_choice) -1['name']]
                except (ValueError, IndexError):
                    print("Invalid selection. Using 'Miscellaneaous'.")
                    new_value = "Miscellaneaous"
        else:
            
            new_value = input(f"Enter new value for {field}: ")

        success, message = self.transaction_manager.edit_transcation(transaction_id, field, new_value)

        if success:
            print("Transaction updated successfully!")
        else:
            print(f"Error: {message}")
    
    def delete_transaction_menu(self):
        """Menu for deleting a transaction."""
        print("\n----- Delete Transaction -----")
        transaction_id = input("Enter transaction ID to delete: ")

        transactions = self.transaction_manager.get_transactions({"id": transaction_id})

        if not transactions:
            print("Transaction not found.")
            return
        
        print("\nTransaction to delete:")
        self.display_transactions(transactions)

        confirm = input("\nAre you sure you want to delete this transaction? (y/n): ")

        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        success, message = self.transaction_manager.delete_transactions(transaction_id)
        
        if success:
            print("Transaction deleted successfully!")
        else:
            print(f"Error: {message}")
    
    def view_categories_menu(self):
        """Menu for view categories."""
        print("\n----- Categories -----")

        print("1. All Categories")
        print("2. Income Categories")
        print("3. Expense Categories")

        choice = input("Enter choice (1-3): ")

        category_type = None
        if choice == "2":
            category_type = "income"
        elif choice == "3":
            category_type = "expense"
        
        categories = self.transaction_manager.category_manager.get_categories(category_type)

        if not categories:
            print("No categories found.")
            return
        
        print(f"\n{'Name':<20} {'Type':<10}")
        print("-" * 30)

        for category in categories:
            print(f"{category['name']:<20} {category['type']:<10}")
    
    def add_category_menu(self):
        """Menu for add a new category."""
        print("\n----- Add New Category -----")

        name = input("Category name: ")
        print("\Category Type:")
        print("1. Income")
        print("2. Expense")
        type_choice = input("Enter choice (1-2): ")
        category_type = "income" if type_choice == "1" else "expense"

        success, message = self.transaction_manager.category_manager.add_category(name, category_type)

        if success:
            print("Category added successfully!")
        else:
            print(f"Error: {message}")
    
    def edit_category(self):
        """Menu for editing a category."""
        print("\n----- Edit Category -----")

        categories = self.transaction_manager.category_manager.get_categories()
        print("\nAvailable Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category['name']} ({category['type']})")

        if not categories:
            print("No categories found.")
            return
        
        category_choice = input(f"Select category to edit (1-{len(categories)}): ")

        try:
            selected_category = categories[int(category_choice) -1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
        
        print(f"\nEditing category: {selected_category['name']} ({selected_category['type']})")

        new_name = input(f"New name [{selected_category['name']}]: ")
        if not new_name:
            new_name = selected_category['name']

        print("\nCategory Type:")
        print(f"1. Income [{selected_category['type'] == 'income' and 'current' or ''}]")
        print(f"2. Expense [{selected_category['type'] == 'expense' and 'current' or ''}]")
        type_choice = input("Enter choice (1-2) [leave blank to keep current]: ")

        if type_choice == "1":
            new_type = "income"
        elif type_choice == "2":
            new_type = "expense"
        else:
            new_type = selected_category['type']

        success, message = self.transaction_manager.category_manager.edit_category(
            selected_category['name'], new_name, new_type
        )

        if success:
            print("Category updated successfully!")
        else:
            print(f"Error: {message}")

    def delete_category_menu(self):
        """Menu for deleting a category."""
        print("\n----- Delete Category -----")

        categories = self.transaction_manager.category_manager.get_categories()
        print("\nAvailable Categories:")
        for i, category in enumerate(categories,1):
            print(f"{i}. {category['name'] ({category['type']})}")

        if not categories:
            print("No categories found.")
            return
        
        category_choice = input(f"Select category to delete (1-{len(categories)}): ")

        try:
            selected_category = categories[int(category_choice) -1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
        
        print(f"\nYou are about to delete category: {selected_category['name']}")
        print("WARNING: This will not delete transactions in this category, but they will have a category that no longer exists.")
        confirm = input("Are you syre? (y/n): ")

        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        success, message = self.transaction_manager.category_manager.delete_category(selected_category['name'])

        if success:
            print("Category deleted successfuly!")
        else:
            print(f"Error: {message}")

    def income_expense_summary(self):
        """Display income vs expenses summary."""
        print("\n----- Income vs Expenses Summary -----")
        
        print("Time period:")
        print("1. This month")
        print("2. Last month")
        print("3. This year")
        print("4. Last year")
        print("5. All time")
        print("6. Custom range")
        
        choice = input("Enter choice (1-6): ")
        
        start_date = None
        end_date = None
        period_name = "All time"
        
        today = datetime.now()
        
        if choice == "1":  # This month
            start_date = datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
            period_name = f"This month ({today.strftime('%B %Y')})"
        elif choice == "2":  # Last month
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            start_date = datetime(last_month_year, last_month, 1).strftime("%Y-%m-%d")
            if last_month == 12:
                end_date = datetime(last_month_year + 1, 1, 1).strftime("%Y-%m-%d")
            else:
                end_date = datetime(last_month_year, last_month + 1, 1).strftime("%Y-%m-%d")
            period_name = f"Last month ({datetime(last_month_year, last_month, 1).strftime('%B %Y')})"
        elif choice == "3":  # This year
            start_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
            period_name = f"This year ({today.year})"
        elif choice == "4":  # Last year
            start_date = datetime(today.year - 1, 1, 1).strftime("%Y-%m-%d")
            end_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
            period_name = f"Last year ({today.year - 1})"
        elif choice == "6":  # Custom range
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
            
            try:
                if start_date:
                    datetime.strptime(start_date, "%Y-%m-%d")
                if end_date:
                    datetime.strptime(end_date, "%Y-%m-%d")
                
                if start_date and end_date:
                    period_name = f"From {start_date} to {end_date}"
                elif start_date:
                    period_name = f"From {start_date}"
                elif end_date:
                    period_name = f"Until {end_date}"
            except ValueError:
                print("Invalid date format. Using all time.")
                start_date = None
                end_date = None
        
        # Get summary
        summary = self.transaction_manager.get_transaction_summary(start_date, end_date)
        
        print(f"\n----- Financial Summary for {period_name} -----")
        print(f"Total Income: ${summary['total_income']:.2f}")
        print(f"Total Expenses: ${summary['total_expenses']:.2f}")
        print(f"Net (Income - Expenses): ${summary['net']:.2f}")
        print(f"Transaction Count: {summary['transaction_count']}")
        
        if summary['total_income'] > 0:
            savings_rate = (summary['net'] / summary['total_income']) * 100
            print(f"Savings Rate: {savings_rate:.2f}%")

    def category_breakdown(self):
        """Display category breakdown report."""
        print("\n----- Category Breakdown -----")
        
        print("Time period:")
        print("1. This month")
        print("2. Last month")
        print("3. This year")
        print("4. Last year")
        print("5. All time")
        print("6. Custom range")
        
        choice = input("Enter choice (1-6): ")
        
        start_date = None
        end_date = None
        period_name = "All time"
        
        today = datetime.now()
        
        if choice == "1":  # This month
            start_date = datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
            period_name = f"This month ({today.strftime('%B %Y')})"
        elif choice == "2":  # Last month
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            start_date = datetime(last_month_year, last_month, 1).strftime("%Y-%m-%d")
            if last_month == 12:
                end_date = datetime(last_month_year + 1, 1, 1).strftime("%Y-%m-%d")
            else:
                end_date = datetime(last_month_year, last_month + 1, 1).strftime("%Y-%m-%d")
            period_name = f"Last month ({datetime(last_month_year, last_month, 1).strftime('%B %Y')})"
        elif choice == "3":  # This year
            start_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
            period_name = f"This year ({today.year})"
        elif choice == "4":  # Last year
            start_date = datetime(today.year - 1, 1, 1).strftime("%Y-%m-%d")
            end_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
            period_name = f"Last year ({today.year - 1})"
        elif choice == "6":  # Custom range
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
            
            # Validate dates
            try:
                if start_date:
                    datetime.strptime(start_date, "%Y-%m-%d")
                if end_date:
                    datetime.strptime(end_date, "%Y-%m-%d")
                
                if start_date and end_date:
                    period_name = f"From {start_date} to {end_date}"
                elif start_date:
                    period_name = f"From {start_date}"
                elif end_date:
                    period_name = f"Until {end_date}"
            except ValueError:
                print("Invalid date format. Using all time.")
                start_date = None
                end_date = None
        
        # Get summary
        summary = self.transaction_manager.get_transaction_summary(start_date, end_date)
        
        print(f"\n----- Category Breakdown for {period_name} -----")
        
        # Get all transactions for the period
        transactions = []
        for transaction in self.transaction_manager.get_transactions():
            transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d")
            
            include = True
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                if transaction_date < start:
                    include = False
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if transaction_date > end:
                    include = False
            
            if include:
                transactions.append(transaction)
        
        # Group transactions by category and type
        income_categories = {}
        expense_categories = {}
        
        for transaction in transactions:
            category = transaction['category']
            amount = transaction['amount']
            
            if transaction['transaction_type'] == 'income':
                if category not in income_categories:
                    income_categories[category] = 0
                income_categories[category] += amount
            else:  # expense
                if category not in expense_categories:
                    expense_categories[category] = 0
                expense_categories[category] += amount
        
        # Display income categories
        if income_categories:
            print("\nINCOME CATEGORIES:")
            print(f"{'Category':<20} {'Amount':<12} {'% of Total':<12}")
            print("-" * 45)
            
            # Sort by amount
            sorted_income = sorted(income_categories.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_income:
                percentage = (amount / summary['total_income']) * 100 if summary['total_income'] > 0 else 0
                print(f"{category:<20} ${amount:<11.2f} {percentage:<11.2f}%")
        
        # Display expense categories
        if expense_categories:
            print("\nEXPENSE CATEGORIES:")
            print(f"{'Category':<20} {'Amount':<12} {'% of Total':<12}")
            print("-" * 45)
            
            # Sort by amount
            sorted_expenses = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_expenses:
                percentage = (amount / summary['total_expenses']) * 100 if summary['total_expenses'] > 0 else 0
                print(f"{category:<20} ${amount:<11.2f} {percentage:<11.2f}%")
    
    def handle_transaction_menu(self):
        """Handle the transaction submenu."""
        while True:
            choice = self.display_transaction_menu()
            
            if choice == "1":
                self.add_transaction_menu()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.search_transactions_menu()
            elif choice == "4":
                self.edit_transaction_menu()
            elif choice == "5":
                self.delete_transaction_menu()
            elif choice == "6":
                return
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def handle_category_menu(self):
        """Handle the category submenu."""
        while True:
            choice = self.display_category_menu()
            
            if choice == "1":
                self.view_categories_menu()
            elif choice == "2":
                self.add_category_menu()
            elif choice == "3":
                self.edit_category_menu()
            elif choice == "4":
                self.delete_category_menu()
            elif choice == "5":
                return
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def handle_report_menu(self):
        """Handle the report submenu."""
        while True:
            choice = self.display_report_menu()
            
            if choice == "1":
                self.income_expense_summary()
            elif choice == "2":
                self.category_breakdown()
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

    def run(self):
        """Run the transaction CLI application."""
        while True:
            choice = self.display_menu()

            if choice == "1":
                self.add_transaction_menu()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.search_transactions_menu()
            elif choice == "4":
                self.edit_transaction_menu()
            elif choice == "5":
                self.delete_transaction_menu()
            elif choice == "6":
                print("Thank you for using Transation Manager. Goodbye!")
                break
            else:
                print("invalid choice, Please try again.")

            input("\nPress Enter to continue...")