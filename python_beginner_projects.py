# python beginner projects 
# Project 1: Simple Calculator
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
def main():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    choice = input("Enter choice (1/2/3/4): ")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    if choice == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == '3':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == '4':
        print(f"{num1} / {num2} = {divide(num1, num2)}")
    else:
        print("Invalid input")
if __name__ == "__main__":
    main()  
# A simple calculator that can perform addition, subtraction, multiplication, and division.
# To use, run the script and follow the prompts to enter two numbers and select an operation.

# End of Project 1: Simple Calculator

# Project 2: Guess the Number
import random
def guess_the_number(): 
    number_to_guess = random.randint(1, 100)
    attempts = 0
    print("Welcome to 'Guess the Number'!")
    print("I'm thinking of a number between 1 and 100.")
    while True:
        guess = int(input("Make a guess: "))
        attempts += 1
        if guess < number_to_guess:
            print("Too low!")
        elif guess > number_to_guess:
            print("Too high!")
        else:
            print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
            break
if __name__ == "__main__":
    guess_the_number()
# A simple number guessing game where the user has to guess a randomly generated number between 1 and 100.
# To use, run the script and follow the prompts to guess the number.

# End of Project 2: Guess the Number

# Project 3: Simple To-Do List
def display_menu():
    print("To-Do List Menu:")
    print("1. View To-Do List")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")
def main():
    todo_list = []
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            if not todo_list:
                print("Your to-do list is empty.")
            else:
                print("Your To-Do List:")
                for idx, task in enumerate(todo_list, start=1):
                    print(f"{idx}. {task}")
        elif choice == '2':
            task = input("Enter the task to add: ")
            todo_list.append(task)
            print(f"'{task}' has been added to your to-do list.")
        elif choice == '3':
            task_number = int(input("Enter the task number to remove: "))
            if 0 < task_number <= len(todo_list):
                removed_task = todo_list.pop(task_number - 1)
                print(f"'{removed_task}' has been removed from your to-do list.")
            else:
                print("Invalid task number.")
        elif choice == '4':
            print("Exiting the To-Do List application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
# A simple to-do list application that allows users to add, view, and remove tasks.
# To use, run the script and follow the prompts to manage your to-do list.

# End of Project 3: Simple To-Do List

# Project 4: Temperature Converter
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9
def main():
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    choice = input("Enter choice (1/2): ")
    if choice == '1':
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = celsius_to_fahrenheit(celsius)
        print(f"{celsius}°C is equal to {fahrenheit}°F")
    elif choice == '2':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        celsius = fahrenheit_to_celsius(fahrenheit)
        print(f"{fahrenheit}°F is equal to {celsius}°C")
    else:
        print("Invalid input")
if __name__ == "__main__":
    main()
# A simple temperature converter that converts between Celsius and Fahrenheit.
# To use, run the script and follow the prompts to enter a temperature and select the conversion type.

# End of Project 4: Temperature Converter

# project 5 tik-tac-toe game
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None
def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True
def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    while True:
        print_board(board)
        row = int(input(f"Player {current_player}, enter your row (0-2): "))
        col = int(input(f"Player {current_player}, enter your column (0-2): "))
        if board[row][col] != " ":
            print("This position is already taken. Try again.")
            continue
        board[row][col] = current_player
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        current_player = "O" if current_player == "X" else "X"
if __name__ == "__main__":
    main()
# A simple Tic-Tac-Toe game for two players.
# To use, run the script and follow the prompts to enter your moves.

# project 6 : Countdown Timer

import time
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02}:{secs:02}'
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print("Time's up!")
def main():
    total_seconds = int(input("Enter the time in seconds for the countdown: "))
    countdown_timer(total_seconds)
if __name__ == "__main__":
    main()
# A simple countdown timer that counts down from a specified number of seconds.
# To use, run the script and enter the number of seconds for the countdown.

# project 7 random password generator

import random
import string
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
def main():
    length = int(input("Enter the desired password length: "))
    password = generate_password(length)
    print(f"Generated password: {password}")
if __name__ == "__main__":
    main()
# A random password generator that creates a password of a specified length using letters, digits, and punctuation.
# To use, run the script and enter the desired password length.
