# My Calculator
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
        return "Division by zero error"
    
# I really struggle with basic math
# Get user input 

# ask for first number
num1 = float(input("Enter first number: "))

# ask for second number
num2 = float(input("Enter second number: "))
# Ask for operation 
operation = input("Enter operation (+, -, *, /): ")
# Do the calculation 
if operation == '+':
    print(f"{num1} + {num2} = {add(num1, num2)}")
elif operation == '-':
    print(f"{num1} - {num2} = {subtract(num1, num2)}")
elif operation == '*':
    print(f"{num1} * {num2} = {multiply(num1, num2)}")
elif operation == '/':
    print(f"{num1} / {num2} = {divide(num1, num2)}")
else:
    print("Invalid operation") 
    # End of calculator.py
# Perform the operation and display the result
