import os
import csv
import uuid
from datetime import datetime

class TransactionManager:
    def  __init__(self, data_dir="data"):
        """Initialize the transaction manager."""
        self.data_dir = data_dir
        self.transactions_file = os.path.join(data_dir, "transactions.csv")
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
                    else:
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

