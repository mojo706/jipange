from transaction_cli import TransactionCLI

def main():
    """Main entry point for Jipange."""
    print("Starting Jipange...")

    # Initialize and run the CLI
    transaction_cli = TransactionCLI()
    transaction_cli.run()

if __name__ == "__main__":
    main()