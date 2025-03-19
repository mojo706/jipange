import os
import csv

class CategoryManager:
    def __init__(self, data_dir="data"):
        """Initialize the category manager."""
        self.data_dir = data_dir
        self.categories_file = os.path.join(data_dir, "categories.csv")
        self.ensure_data_directory()
        self.initialize_categories_file()

    def ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)

    def initialize_categories_file(self):
        """Initialize the categories file with default categories if it doesn't exist."""
        if not os.path.exists(self.categories_file):
            default_categories = [
                # Income categories
                "Salary", "Bonus", "Investment", "Gift", "Refund", "Other Income",

                # Expense categories
                "Housing", "Utilities", "Groceries", "Dining Out", "Transportation",
                "Entertainment", "Shopping", "Health", "Education", "Personal Care",
                "Travel", "Gifts", "Charity", "Insurance", "Taxes", "Debt Payment", 
                "Savings", "Miscellaneous"
            ]

            with open(self.categories_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["name", "type"])

                # Add income categories

                for category in default_categories[:6]:
                    writer.writerow([category, "income"])

                # Add expense categories
                for category in default_categories[6:]:
                    writer.writerow([category, "expense"])
    
    def get_categories(self, transaction_type=None):
        """Get all categories or filter by transaction type."""
        categories = []
        try:
            with open(self.categories_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if transaction_type is None or row['type'] == transaction_type:
                        categories.append(row)
            return categories
        except Exception as e:
            print(f"Error retrieving categories: {str(e)}")
            return []
    
    def add_category(self, name, category_type):
        """Add a new category."""
        try:

            # Validate category type
            if category_type not in ["income", "expense"]:
                return False, "Category type must be either 'income' or 'expense'"
            
            # Check if category already exists
            existing_categories = self.get_categories()
            for category in existing_categories:
                if category['name'].lower() == name.lower():
                   return False, "Category already exists"

            # Add the new category
            with open(self.categories_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, category_type])

            return True, "Category added successfully"
        except Exception as e:
            return False, f"Error adding category: {str(e)}"
    
    def delete_category(self, name):
        """Delete a category."""
        try:
            categories = self.get_categories()
            filtered_categories = [c for c in categories if c['name'].lower() != name.lower()]

            if len(filtered_categories) == len(categories):
                return False, "Category not found"
            
            # Write back all the categories except the deleted one
            with open(self.categories_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["name", "type"])
                writer.writeheader()
                for category in filtered_categories:
                    writer.writerow(category)

            return True, "Category deleted successfully"
        except Exception as e:
            return False, f"Error deleting category: {str(e)}"
        
    def edit_category(self, old_name, new_name, new_type="None"):
        """Edit a category name and optionally its type."""
        try:
            categories = self.get_categories()
            found = False
            
            for category in categories:
                if category['name'].lower() == old_name.lower():
                    category['name'] = new_name
                    if new_type:
                        if new_type not in ["income", "expense"]:
                            return False, "Category type must be either 'income' or 'expense'"
                        category['type'] = new_type
                    found = True
                    break

            if not found:
                return False, "Category not found"
            
            # Write back all categories with the edited one
            with open(self.categories_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["name", "type"])
                writer.writeheader()
                for category in categories:
                    writer.writerow(category)

            return True, "Category updated successfully"
        except Exception as e:
            return False, f"Error editing category: {str(e)}"
