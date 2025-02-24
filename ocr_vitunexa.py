import pytesseract
from PIL import Image
import re
import sqlite3
import pandas as pd

# Set up SQLite Database
def create_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, date TEXT, category TEXT)''')
    conn.commit()
    conn.close()

# Function to scan receipt and extract text using OCR
def scan_receipt(image_path):
    # Load the image
    image = Image.open(image_path)
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)
    return text

# Function to extract relevant data from receipt text (using regex)
def extract_data(receipt_text):
    # Example regex to extract total amount and date
    amount = re.search(r'Total:\s?\$(\d+\.\d{2})', receipt_text)
    date = re.search(r'Date:\s?(\d{2}/\d{2}/\d{4})', receipt_text)
    
    if amount and date:
        return {
            'amount': amount.group(1),
            'date': date.group(1)
        }
    return None

# Functions for basic arithmetic operations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero"

# Save expense data to SQLite database
def save_expense(amount, date, category):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, date, category) VALUES (?, ?, ?)", (amount, date, category))
    conn.commit()
    conn.close()

# Function to generate a report of expenses by category
def generate_report():
    conn = sqlite3.connect('expenses.db')
    query = "SELECT * FROM expenses"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Generate a summary of expenses by category
    report = df.groupby('category')['amount'].sum()
    print(report)
    return report

# Console-based user interface
def main():
    # Create the database if it doesn't exist
    create_db()

    while True:
        print("\nOptions: \n1. Scan Receipt\n2. Add Expense\n3. Perform Arithmetic Operation\n4. Generate Report\n5. Exit")
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            image_path = input("Enter the path of the receipt image: ")
            receipt_text = scan_receipt(image_path)
            print("Receipt Text Extracted:")
            print(receipt_text)

            # Extract data from receipt
            data = extract_data(receipt_text)
            if data:
                print(f"Amount: {data['amount']}, Date: {data['date']}")
                category = input("Enter category for this expense: ")
                save_expense(data['amount'], data['date'], category)
            else:
                print("Could not extract valid data from receipt.")

        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            date = input("Enter expense date (MM/DD/YYYY): ")
            category = input("Enter category for this expense: ")
            save_expense(amount, date, category)
            print("Expense added successfully.")

        elif choice == '3':
            print("\nArithmetic Operations: \n1. Add\n2. Subtract\n3. Multiply\n4. Divide")
            operation = input("Choose operation (1-4): ")

            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if operation == '1':
                    print(f"Result: {add(num1, num2)}")
                elif operation == '2':
                    print(f"Result: {subtract(num1, num2)}")
                elif operation == '3':
                    print(f"Result: {multiply(num1, num2)}")
                elif operation == '4':
                    print(f"Result: {divide(num1, num2)}")
                else:
                    print("Invalid operation choice.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")

        elif choice == '4':
            generate_report()

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
