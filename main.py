from transaction_cli import TransactionCLI
import os

def main():
    """Main entry point for the Personal Finance Manager application."""
    # Clear the screen for a better UI experience
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("===================================")
    print("  JIPANGE v1.0")
    print("===================================")
    print("Starting Jipange ...")
    print("\nThis application will help you track your finances,")
    print("manage your transactions, and analyze your spending patterns.")
    print("\nAll data is stored locally in CSV files in the 'data' directory.")
    
    # Initialize and run the CLI
    transaction_cli = TransactionCLI()
    transaction_cli.run()

if __name__ == "__main__":
    main()