import PyPDF2
import sqlite3
import tkinter as tk
from tkinter import messagebox

# --- PDF Merge and Split Functions ---

def merge_pdfs(pdf_list, output_filename):
    """Merge multiple PDF files into one"""
    pdf_writer = PyPDF2.PdfWriter()
    
    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_filename, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    print(f'Merged PDF saved as {output_filename}')
    messagebox.showinfo("Success", f"Merged PDF saved as {output_filename}")

def split_pdf(input_pdf, output_dir):
    """Split a single PDF into individual pages"""
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output_filename = f"{output_dir}/page_{page_num + 1}.pdf"
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        print(f'Saved page {page_num + 1} as separate PDF')
        messagebox.showinfo("Success", f"Page {page_num + 1} saved successfully")

# --- Calculator Functions ---

# Basic arithmetic operations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

# SQLite History Function
def save_history(operation, result):
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (operation TEXT, result TEXT)''')
    c.execute('''INSERT INTO history (operation, result)
                 VALUES (?, ?)''', (operation, result))
    conn.commit()
    conn.close()

# --- Console-based Calculator UI ---

def calculator_ui():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    
    choice = input("Enter choice (1/2/3/4/5): ")
    
    if choice == '5':
        print("Exiting calculator.")
        return
    
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return
    
    if choice == '1':
        result = add(num1, num2)
        operation = f"{num1} + {num2}"
    elif choice == '2':
        result = subtract(num1, num2)
        operation = f"{num1} - {num2}"
    elif choice == '3':
        result = multiply(num1, num2)
        operation = f"{num1} * {num2}"
    elif choice == '4':
        result = divide(num1, num2)
        operation = f"{num1} / {num2}"
    else:
        print("Invalid input")
        return

    print(f"Result: {result}")
    save_history(operation, result)

# --- Tkinter-based Calculator GUI ---

def gui_add():
    try:
        result_var.set(float(entry1.get()) + float(entry2.get()))
    except ValueError:
        result_var.set("Error! Invalid input.")

def gui_subtract():
    try:
        result_var.set(float(entry1.get()) - float(entry2.get()))
    except ValueError:
        result_var.set("Error! Invalid input.")

def gui_multiply():
    try:
        result_var.set(float(entry1.get()) * float(entry2.get()))
    except ValueError:
        result_var.set("Error! Invalid input.")

def gui_divide():
    try:
        divisor = float(entry2.get())
        if divisor == 0:
            result_var.set("Error! Division by zero.")
        else:
            result_var.set(float(entry1.get()) / divisor)
    except ValueError:
        result_var.set("Error! Invalid input.")

def open_pdf_tools():
    choice = input("Choose PDF operation:\n1. Merge PDFs\n2. Split PDF\nEnter choice: ")
    
    if choice == '1':
        pdf_list = input("Enter list of PDF file paths (comma-separated): ").split(",")
        output_filename = input("Enter output filename (with .pdf extension): ")
        merge_pdfs(pdf_list, output_filename)
    elif choice == '2':
        input_pdf = input("Enter the PDF file path to split: ")
        output_dir = input("Enter the output directory for split pages: ")
        split_pdf(input_pdf, output_dir)
    else:
        print("Invalid choice!")

# --- Tkinter Setup ---

window = tk.Tk()
window.title("Calculator")

# Define GUI components
entry1 = tk.Entry(window)
entry2 = tk.Entry(window)
result_var = tk.StringVar()

result_label = tk.Label(window, text="Result:")
result_display = tk.Label(window, textvariable=result_var)

add_button = tk.Button(window, text="+", command=gui_add)
subtract_button = tk.Button(window, text="-", command=gui_subtract)
multiply_button = tk.Button(window, text="*", command=gui_multiply)
divide_button = tk.Button(window, text="/", command=gui_divide)

# Place components on the window
entry1.grid(row=0, column=0)
entry2.grid(row=0, column=1)
add_button.grid(row=1, column=0)
subtract_button.grid(row=1, column=1)
multiply_button.grid(row=2, column=0)
divide_button.grid(row=2, column=1)
result_label.grid(row=3, column=0)
result_display.grid(row=3, column=1)

# Provide an option to open PDF tools
pdf_button = tk.Button(window, text="Open PDF Tools", command=open_pdf_tools)
pdf_button.grid(row=4, column=0, columnspan=2)

# Start the Tkinter loop
window.mainloop()

# --- Main Program Execution ---

if __name__ == "__main__":
    print("Welcome to the PDF and Calculator Tool!")
    print("Type 'gui' to open the GUI-based calculator, or 'cli' for the console-based calculator.")
    choice = input("Enter choice (gui/cli): ").lower()
    
    if choice == 'cli':
        while True:
            calculator_ui()
    elif choice == 'gui':
        window.mainloop()
    else:
        print("Invalid choice! Exiting program.")
