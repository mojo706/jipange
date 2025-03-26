import os
import csv
import uuid
from datetime import datetime
from category_manager import CategoryManager

class TransactionManager:
    def  __init__(self, data_dir="data"):
        """Initialize the transaction manager."""
        self.data_dir = data_dir
        self.transactions_file = os.path.join(data_dir, "transactions.csv")
        self.category_manager = CategoryManager(data_dir)
        self.ensure_data_directory()
        self.initialize_transactions_file()

    def ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)

    def initialize_transactions_file(self):
        """Initialize the transactions file with headers if it doesn't exist"""
        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "date", "amount", "category", "account", "description", "transaction_type"])
    
    def add_transaction(self, date, amount, category, account, description, transaction_type):
        """Add a new transaction to the system. """
        try:
            # Validate date format
            if date:
                datetime.strptime(date, "%Y-%m-%d")
            else:
                date = datetime.now().strftime("%Y-%m-%d")

            # Validate amount
            try:
                amount = float(amount)
                if amount <= 0:
                    return False, "Amount must be greater than zero."
            except ValueError:
                return False, "Amount must be a valid number."
            
            # Validate transaction type
            if transaction_type not in ["income", "expense"]:
                return False, "Transaction type must be either 'income' or 'expense'."
            
            # Validate category and account
            if not category or not account:
                return False, "Category and account are empty."
            
            # Check if the transaction exists and matches the transaction type
            categories = self.category_manager.get_categories(transaction_type)
            category_exists = any(c['name'].lower() == category.lower() for c in categories)

            if not category_exists:
                # Ask the category manager to add this as a new category
                self.category_manager.add_category(category, transaction_type)
            
            #Generate unique ID
            transaction_id = str(uuid.uuid4())

            # Write to file
            with open(self.transactions_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([transaction_id, date, amount, category, account, description, transaction_type])
            
            return True, f"Transaction added successfully with ID: {transaction_id}"

        except ValueError as e:
            return False, f"Invalid date format: {e}"
        except Exception as e:
            return False, f"Error adding transaction: {str(e)}"
        
    def get_transactions(self, filters=None):
        """Get transactions with optional filtering."""
        transactions = []
        try:
            if not os.path.exists(self.transactions_file):
                return []
            
            with open(self.transactions_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Apply filters if provided
                    if filters:
                        include = True
                        for key, value in filters.items():
                            if key in row and str(row[key]).lower() != str(value).lower():
                                include = False
                                break
                        if not include:
                            continue
                    
                    #Convert amount to float for calculations
                    row['amount'] = float(row['amount'])
                    transactions.append(row)

            return transactions
        except Exception as e:
            print(f"Error retrieving transactions: {str(e)}")
            return []
    
    def delete_transactions(self, transaction_id):
        """Delete a transaction by ID."""
        try:
            transactions = self.get_transactions()
            filtered_transactions = [t for t in transactions if t['id'] != transaction_id]

            if len(filtered_transactions) == len(transactions):
                return False, "Transaction not found"
            
            # Write back all transactions except the deleted one
            with open(self.transactions_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "date", "amount", "category","account", "description", "transaction_type"])
                writer.writeheader()
                for transaction in filtered_transactions:
                    writer.writerow(transaction)
            
            return True, "Transaction deleted successfully"
        except Exception as e:
            return False, f"Error deleting transaction: {str(e)}"
    
    def edit_transcation(self, transaction_id, field, new_value):
        """Edit a specific field of a transaction."""
        try:
            transactions = self.get_transactions()
            found = False
            
            for transaction in transactions:
                if transaction['id'] == transaction_id:

                    # Validate field
                    if field not in transaction:
                        return False, f"Invalid field: {field}"
                    
                    #Special validation for certain fields
                    if field == "date":
                        datetime.strptime(new_value, "%Y-%m-%d")
                    elif field == "amount":
                        transaction[field] = float(new_value)
                    elif field == "transaction_type" and new_value not in ["income", "expense"]:
                        return False, "Transaction type must be either 'income' or 'expense'"
                    elif field == "category":
                        # Check if the category exists and matches the transaction type
                        categories = self.category_manager.get_categories(transaction['transaction_type'])
                        category_exists = any(c['name'].lower() == new_value.lower() for c in categories)

                        if not category_exists:
                            # Ask the category manager to add this as a new category
                            self.category_manager.add_category(new_value, transaction['transaction_type'])

                    transaction[field] = new_value
                    found = True
                    break

            if not found:
                return False, "Transaction not found"

            # Write back all the transactions with the edited one
            with open(self.transactions_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "date", "amount", "category", "account", "description", "transacation_type"])
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow(transaction)
            
            return True, "Transaction updated successfully"
        except ValueError as e:
            return False, f"Invalid value format: {str(e)}"
        except Exception as e:
            return False, f"Error editing transaction: {str(e)}"
        
    def search_transactions(self, keyword):
        result = []
        transactions = self.get_transactions()

        keyword = str(keyword).lower()

        for transaction in transactions:
            for field, value in transaction.items():
                if keyword in str(value).lower():
                    result.append(transaction)
                    break
        
        return result
    
    def get_transaction_summary(self, start_date=None, end_date=None):
        """Get a summary of transactions withing a date range"""
        transactions = self.get_transactions()
        filtered_transactions = []

        # Filter by date if provided
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%/d")

            if start_date and end_date:
                start = datetime.strptime(start_date, "%Y-%m-%/d")
                end  = datetime.strptime(end_date, "%Y-%m-%/d")
                if start <= transaction_date <= end:
                    filtered_transactions.append(transaction)
            elif start_date:
                start = datetime.strptime(start_date, "%Y-%m-%/d")
                if start <= transaction_date:
                    filtered_transactions.append(transaction)
            else:
                filtered_transactions.append(transaction)

        # Calculate summary statistics
        total_income = sum(t['amount'] for t in filtered_transactions if t['transaction_type'] == 'income')
        total_expenses = sum(t['amount'] for t in filtered_transactions if t['transaction_type'] == 'expense')
        net = total_income - total_expenses

        # Group by category
        categories = {}
        for transaction in filtered_transactions:
            category = transaction['category']
            if category not in categories:
                categories[category] = 0
            categories[category] += transaction['amount']
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': net,
            'categories': categories,
            'transaction_count': len(filtered_transactions)
        }

