---
marp: true
theme: default
paginate: true
header: 'Python II: การควบคุมและฟังก์ชัน'
footer: 'Week 2 | 11/8/2025'
---

<!-- _class: lead -->
# Python II: การควบคุมและฟังก์ชัน
## Python II: Control Flow and Functions

**สัปดาห์ที่ 2 | Week 2**
วันที่ 8 พฤศจิกายน 2025

---

## เนื้อหาในวันนี้ | Today's Agenda

1. 🔀 Conditional Statements (if/elif/else)
2. 🔁 Loops (for and while)
3. 🎯 Functions and Parameters
4. 📦 Scope and Return Values
5. 💻 Hands-on Examples
6. 🎯 Practice Exercises

---

<!-- _class: lead -->
# 🔀 Conditional Statements
## คำสั่งควบคุมเงื่อนไข

---

## If Statement

```python
age = 18

if age >= 18:
    print("You are an adult")
    print("You can vote!")
```

**Key Points:**
- Condition must evaluate to `True` or `False`
- Code block must be indented (4 spaces or 1 tab)
- Colon `:` is required after the condition

---

## If-Else Statement

```python
temperature = 35

if temperature > 30:
    print("It's hot! 🌡️")
else:
    print("Weather is nice 😊")

# Example with user input
password = input("Enter password: ")

if password == "secret123":
    print("✅ Access granted")
else:
    print("❌ Access denied")
```

---

## If-Elif-Else Statement

```python
score = 85

if score >= 80:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 60:
    grade = "C"
elif score >= 50:
    grade = "D"
else:
    grade = "F"

print(f"Your grade: {grade}")
```

**Note:** Once a condition is `True`, remaining conditions are skipped.

---

## Nested If Statements

```python
age = 20
has_license = True

if age >= 18:
    if has_license:
        print("You can drive! 🚗")
    else:
        print("You need a license first")
else:
    print("You're too young to drive")

# Better way using logical operators
if age >= 18 and has_license:
    print("You can drive! 🚗")
else:
    print("You cannot drive")
```

---

## Conditional Expressions (Ternary Operator)

```python
# Traditional if-else
age = 20
if age >= 18:
    status = "Adult"
else:
    status = "Minor"

# Ternary operator (one-liner)
status = "Adult" if age >= 18 else "Minor"

# More examples
max_value = a if a > b else b
message = "Pass" if score >= 50 else "Fail"
discount = 0.1 if is_member else 0
```

---

<!-- _class: lead -->
# 🔁 Loops
## การวนซ้ำ

---

## For Loop - Basics

```python
# Loop through a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop through a string
for char in "Python":
    print(char)

# Loop with range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Range with start and end
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5

# Range with step
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
```

---

## For Loop - Advanced

```python
# Loop with enumerate (get index and value)
fruits = ["apple", "banana", "orange"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Loop through dictionary
student = {"name": "Alice", "age": 20, "gpa": 3.75}
for key, value in student.items():
    print(f"{key}: {value}")

# Loop with zip (combine multiple lists)
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 88]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

---

## While Loop

```python
# Basic while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# User input validation
password = ""
while password != "secret":
    password = input("Enter password: ")
    if password != "secret":
        print("Wrong password, try again")

print("Access granted!")

# Infinite loop with break
while True:
    command = input("Enter command (q to quit): ")
    if command == "q":
        break
    print(f"You entered: {command}")
```

---

## Loop Control: Break and Continue

```python
# Break - exit the loop
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# Continue - skip current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4

# Example: Find first even number
numbers = [1, 3, 5, 8, 9, 10]
for num in numbers:
    if num % 2 == 0:
        print(f"First even number: {num}")
        break
```

---

## Loop with Else Clause

```python
# Else clause executes if loop completes without break
numbers = [1, 3, 5, 7, 9]
for num in numbers:
    if num % 2 == 0:
        print(f"Found even number: {num}")
        break
else:
    print("No even numbers found")

# While loop with else
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("Loop completed!")
```

---

## Nested Loops

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")

# Pattern printing
for i in range(5):
    for j in range(i + 1):
        print("*", end="")
    print()

# Output:
# *
# **
# ***
# ****
# *****
```

---

<!-- _class: lead -->
# 🎯 Functions
## ฟังก์ชัน

---

## Defining Functions

```python
# Basic function
def greet():
    print("Hello, World!")

greet()  # Call the function

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

# Function with multiple parameters
def add(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")

add(5, 3)
add(10, 20)
```

---

## Return Values

```python
# Function that returns a value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8

# Return multiple values
def get_user_info():
    name = "Alice"
    age = 20
    return name, age

name, age = get_user_info()
print(f"{name} is {age} years old")

# Early return
def check_age(age):
    if age < 18:
        return "Minor"
    return "Adult"
```

---

## Default Parameters

```python
# Default parameter values
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")          # Hi, Bob!

# Multiple defaults
def create_profile(name, age=18, city="Bangkok"):
    return {
        "name": name,
        "age": age,
        "city": city
    }

profile1 = create_profile("Alice")
profile2 = create_profile("Bob", 25)
profile3 = create_profile("Charlie", 30, "Chiang Mai")
```

---

## Keyword Arguments

```python
# Named arguments
def create_user(name, age, email):
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Email: {email}")

# Position-based call
create_user("Alice", 20, "alice@email.com")

# Keyword-based call (order doesn't matter)
create_user(email="bob@email.com", name="Bob", age=25)

# Mix of both
create_user("Charlie", email="charlie@email.com", age=30)
```

---

## *args and **kwargs

```python
# *args - variable number of positional arguments
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs - variable number of keyword arguments
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=20, city="Bangkok")
```

---

## Lambda Functions

```python
# Regular function
def square(x):
    return x ** 2

# Lambda function (anonymous function)
square = lambda x: x ** 2

print(square(5))  # 25

# Lambda with multiple parameters
add = lambda a, b: a + b
print(add(3, 5))  # 8

# Lambda in sorted()
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]
sorted_students = sorted(students, key=lambda s: s["score"], reverse=True)
```

---

## Scope - Local and Global

```python
# Global variable
x = 10

def function1():
    # Local variable
    y = 5
    print(f"Inside function: x={x}, y={y}")

function1()
print(f"Outside function: x={x}")
# print(y)  # Error: y is not defined outside function

# Modifying global variable
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1
```

---

## Docstrings

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Parameters:
    length (float): Length of the rectangle
    width (float): Width of the rectangle
    
    Returns:
    float: Area of the rectangle
    """
    return length * width

# Access docstring
print(calculate_area.__doc__)

# Help function
help(calculate_area)
```

---

<!-- _class: lead -->
# 💻 Hands-on Examples
## ตัวอย่างการใช้งาน

---

## Example 1: Grade Calculator with Functions

```python
def calculate_grade(score):
    """Calculate letter grade from numeric score"""
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else: 
        return "F"

def calculate_average(scores):
    """Calculate average of a list of scores"""
    return sum(scores) / len(scores)

# Use the functions
student_scores = [85, 90, 78, 92, 88]
average = calculate_average(student_scores)
grade = calculate_grade(average)

print(f"Scores: {student_scores}")
print(f"Average: {average:.2f}")
print(f"Grade: {grade}")
```

---

## Example 2: Todo List Manager

```python
def add_task(todo_list, task):
    """Add a task to the todo list"""
    todo_list.append(task)
    print(f"✅ Added: {task}")

def remove_task(todo_list, task):
    """Remove a task from the todo list"""
    if task in todo_list:
        todo_list.remove(task)
        print(f"✅ Removed: {task}")
    else:
        print(f"❌ Task not found: {task}")

def show_tasks(todo_list):
    """Display all tasks"""
    print("\n📋 Todo List:")
    if not todo_list:
        print("  (empty)")
    for i, task in enumerate(todo_list, 1):
        print(f"  {i}. {task}")

# Use the functions
tasks = []
add_task(tasks, "Study Python")
add_task(tasks, "Buy groceries")
show_tasks(tasks)
remove_task(tasks, "Study Python")
show_tasks(tasks)
```

---

## Example 3: Number Guessing Game

```python
import random

def play_game():
    """Number guessing game"""
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print("🎮 Guess the number between 1 and 100!")
    print(f"You have {max_attempts} attempts.")
    
    while attempts < max_attempts:
        guess = int(input("\nYour guess: "))
        attempts += 1
        
        if guess == secret_number:
            print(f"🎉 Correct! You won in {attempts} attempts!")
            return True
        elif guess < secret_number:
            print("📈 Too low!")
        else:
            print("📉 Too high!")
        
        print(f"Attempts remaining: {max_attempts - attempts}")
    
    print(f"\n😢 Game over! The number was {secret_number}")
    return False

play_game()
```

---

## Example 4: Menu-Driven Calculator

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def calculator():
    print("🧮 Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    
    choice = input("\nChoose operation (1-4): ")
    
    if choice in ['1', '2', '3', '4']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        if choice == '1':
            print(f"Result: {add(num1, num2)}")
        elif choice == '2':
            print(f"Result: {subtract(num1, num2)}")
        elif choice == '3':
            print(f"Result: {multiply(num1, num2)}")
        else:
            print(f"Result: {divide(num1, num2)}")
    else:
        print("Invalid choice")

calculator()
```

---

<!-- _class: lead -->
# 🎯 Practice Exercises
## แบบฝึกหัด

---

## Exercise 1: FizzBuzz

Write a program that prints numbers from 1 to 100:
- Print "Fizz" for multiples of 3
- Print "Buzz" for multiples of 5
- Print "FizzBuzz" for multiples of both 3 and 5
- Otherwise, print the number

```python
# Your code here
for i in range(1, 101):
    # TODO: Implement FizzBuzz logic
    pass
```

---

## Exercise 2: Temperature Converter

Create functions to convert temperatures:
- `celsius_to_fahrenheit(celsius)`
- `fahrenheit_to_celsius(fahrenheit)`

Formula:
- F = C × 9/5 + 32
- C = (F - 32) × 5/9

```python
# TODO: Implement the functions

# Test your functions
print(celsius_to_fahrenheit(0))   # Should be 32
print(fahrenheit_to_celsius(32))  # Should be 0
```

---

## Exercise 3: Find Prime Numbers

Write a function that checks if a number is prime, then find all prime numbers between 1 and 100.

```python
def is_prime(n):
    """Check if n is a prime number"""
    # TODO: Implement prime checking logic
    pass

# Find all primes between 1 and 100
primes = []
for num in range(2, 101):
    if is_prime(num):
        primes.append(num)

print(f"Prime numbers: {primes}")
```

---

## Exercise 4: Password Validator

Create a function that validates a password. A valid password must:
- Be at least 8 characters long
- Contain at least one uppercase letter
- Contain at least one lowercase letter
- Contain at least one digit

```python
def validate_password(password):
    """Validate password strength"""
    # TODO: Implement validation logic
    pass

# Test cases
print(validate_password("weak"))         # False
print(validate_password("Strong123"))    # True
```

---

## Exercise 5: List Statistics

Write functions to calculate statistics from a list of numbers:
- `calculate_mean(numbers)` - average
- `calculate_median(numbers)` - middle value
- `calculate_mode(numbers)` - most common value

```python
def calculate_mean(numbers):
    # TODO: Implement
    pass

def calculate_median(numbers):
    # TODO: Implement
    pass

def calculate_mode(numbers):
    # TODO: Implement
    pass

# Test with data
data = [5, 2, 8, 2, 9, 2, 3, 7]
```

---

<!-- _class: lead -->
# 📚 Summary
## สรุป

---

## What We Learned Today

**1. Conditional Statements:**
- `if`, `elif`, `else`
- Nested conditions
- Ternary operators

**2. Loops:**
- `for` loops with range, lists, dictionaries
- `while` loops
- `break`, `continue`, and `else` clause
- Nested loops

---

## What We Learned Today (cont.)

**3. Functions:**
- Defining and calling functions
- Parameters and return values
- Default parameters and keyword arguments
- `*args` and `**kwargs`
- Lambda functions
- Variable scope

**4. Best Practices:**
- Use descriptive function names
- Add docstrings for documentation
- Keep functions focused on single tasks
- Avoid global variables when possible

---

## Next Week Preview

**สัปดาห์ที่ 3: Program Planning and Design**
- Problem analysis
- Flowcharts and pseudocode
- Breaking down complex problems
- Planning before coding

---

<!-- _class: lead -->
# 🙏 Thank You!
## Questions?

**Happy Coding! 🐍**

