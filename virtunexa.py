import time
import threading
import sys

def countdown_timer(total_seconds):
    """Countdown from total_seconds to 0 and print time updates."""
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        timer_str = f"{mins:02d}:{secs:02d}"
        print(timer_str, end='\r')
        time.sleep(1)
        total_seconds -= 1
    print("\nTime's up! Countdown finished.")

def start_countdown():
    try:
        unit = input("Enter duration unit (M for minutes, S for seconds): ").strip().upper()
        duration = float(input("Enter duration: ").strip())
    except ValueError:
        print("Invalid input. Please enter a numeric value for duration.")
        return

    if unit == 'M':
        total_seconds = int(duration * 60)
    elif unit == 'S':
        total_seconds = int(duration)
    else:
        print("Invalid unit. Please enter 'M' for minutes or 'S' for seconds.")
        return

    # Start countdown in a separate thread
    timer_thread = threading.Thread(target=countdown_timer, args=(total_seconds,))
    timer_thread.start()
    timer_thread.join()  # Wait for the countdown to finish

def basic_calculator():
    """Performs basic arithmetic operations and logs the result."""
    try:
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, -, *, /): ").strip()
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    result = None
    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: Division by zero.")
                return
            result = num1 / num2
        else:
            print("Invalid operator. Please use one of: +, -, *, /")
            return
    except Exception as e:
        print("An error occurred:", e)
        return

    print(f"Result: {result}")
    # Log the calculation to a file
    try:
        with open("calculator_history.txt", "a") as log_file:
            log_file.write(f"{num1} {operator} {num2} = {result}\n")
    except Exception as e:
        print("Error logging the operation:", e)

def main():
    while True:
        print("\n==== Multi-Function Application ====")
        print("1. Countdown Timer")
        print("2. Calculator")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            start_countdown()
        elif choice == '2':
            basic_calculator()
        elif choice == '3':
            print("Exiting application.")
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
