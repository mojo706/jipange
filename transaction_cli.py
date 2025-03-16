from transaction_manager import TransactionManager
from datetime import datetime

class TransactionCLI:
    def __init__(self):
        """Initialize the transaction CLI."""
        self.transaction_manager = TransactionManager()
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n===== Jipange =====")
        print("1. Add new transaction")
        print("2. View all transactions")
        print("3. Search transactions")
        print("4. Edit transactions")
        print("5. Delete transaction")
        print("6. Exit")
        return input("Enter your choice (1-6): ")
    
    def add_transaction_menu(self):
        """Menu for adding a new transaction."""
        print("\n----- Add New Transaction -----")

        #Get transaction details from user
        date_input = input("Date (YYYY-MM-DD) [today]: ")
        if not date_input:
            date_input = datetime.now().strftime("%Y-%m-%\d")
        
        amount_input = input("Amount: ")

        # Transaction tyoe
        print("\nTransaction Type: ")
        print("1. Income")
        print("2. Expense")
        type_choice = input("Emter choice (1-2): ")
        transaction_type = "income" if type_choice == "1" else "expense"

        # Get category
        category = input("Category (e.g., Food, Rent, Salary): ")

        # Get account
        account = input("Account (e.g., Cash, Checking, Credit Card): ")

        # Get description
        description = input("Description: ")

        # Add transaction
        success, message = self.transaction_manager.add_transaction(date_input, amount_input, category, account, description, transaction_type)

        if success:
            print("Transaction added Successfully")
        else:
            print(f"Error: {message}")
    
    def view_transactions(self):
        """View all transactions with simple filtering options."""
        print("\n----- Transaction History -----")

        transactions = self.transaction_manager.get_transactions()

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

        # Find the transaction
        transactions = self.transaction_manager.get_transactions({"id": transaction_id})

        if not transactions:
            print("Transaction not found.")
            return
        
        #Display the transaction
        print("\nCurrent transaction details:")
        self.display_transactions(transactions)

        # Ask which field to edit
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

        # Get new value
        new_value = input(f"Enter new value for {field}: ")

        # For transaction type, provide options
        if field == "transaction_type":
            print("1. Income")
            print("2. Expense")
            type_choice = input("Enter choice (1-2): ")
            new_value = "income" if type_choice == "1" else "expense"

        # Update the transaction
        success, message = self.transaction_manager.edit_transcation(transaction_id, field, new_value)

        if success:
            print("Transaction updated successfully!")
        else:
            print(f"Error: {message}")
    
    def delete_transaction_menu(self):
        """Menu for deleting a transaction."""
        print("\n----- Delete Transaction -----")
        transaction_id = input("Enter transaction ID to delete: ")

        # Find the transaction
        transactions = self.transaction_manager.get_transactions({"id": transaction_id})

        if not transactions:
            print("Transaction not found.")
            return
        
        # Display the transaction
        print("\nTransaction to delete:")
        self.display_transactions(transactions)

        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this transaction? (y/n): ")

        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        # Delete the transaction
        success, message = self.transaction_manager.delete_transactions(transaction_id)
        
        if success:
            print("Transaction deleted successfully!")
        else:
            print(f"Error: {message}")

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