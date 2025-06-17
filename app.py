from data_manager import add_record, view_records
from datetime import datetime

def add_new_record_ui():
    """Prompts user for record details and adds it."""
    print("\n--- Add New Record ---")
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break # Valid date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    description = input("Enter description: ")
    while True:
        type_str = input("Enter type (income/expense): ").lower()
        if type_str in ['income', 'expense']:
            break
        else:
            print("Invalid type. Please enter 'income' or 'expense'.")
    while True:
        amount_str = input("Enter amount: ")
        try:
            amount = float(amount_str)
            if amount > 0:
                break
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    add_record(date_str, description, type_str, amount)
    print("Record added successfully!")

def view_all_records_ui():
    """Displays all records to the user."""
    print("\n--- View All Records ---")
    records = view_records()
    if records:
        print(f"{'Date':<12} | {'Description':<30} | {'Type':<10} | {'Amount':>10}")
        print("-" * 70)
        for record in records:
            print(f"{record.get('date', 'N/A'):<12} | {record.get('description', 'N/A'):<30} | {record.get('type', 'N/A'):<10} | {record.get('amount', 'N/A'):>10.2f}")
    else:
        # Message is printed by view_records if no records are found or file is empty/corrupted
        pass # Or print a generic "No records to display." if preferred

def main_menu():
    """Displays the main menu and handles user interaction."""
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add new record")
        print("2. View all records")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_record_ui()
        elif choice == '2':
            view_all_records_ui()
        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
