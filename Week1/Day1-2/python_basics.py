# python_basics.py - My experiments with Python basics

# Exploring Variables and Data Types
print("1. My Variable and Data Type Experiments")

# Testing out integers
my_age = 28
print(f"My age (integer): {my_age}")

# Trying floats
my_height = 1.89
print(f"My height in meters (float): {my_height}")

# Playing with strings
my_name = "Edoardo"
print(f"My name (string): {my_name}")

# Understanding booleans
am_i_learning = True
print(f"Am I learning? (boolean): {am_i_learning}")

# Experimenting with lists
my_favorite_foods = ["pizza", "sushi", "pasta"]
print(f"My favorite foods (list): {my_favorite_foods}")

# Trying out dictionaries
about_me = {"name": my_name, "age": my_age, "city": "Everywhere"}
print(f"About me (dictionary): {about_me}")

print("\n2. My Basic Operation Experiments")

# Testing arithmetic operations
a, b = 10, 3
print(f"a = {a}, b = {b}")
print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")
print(f"Division: {a / b}")
print(f"Integer Division: {a // b}")
print(f"Modulus: {a % b}")
print(f"Exponentiation: {a ** b}")

# Trying string operations
my_first_name = "John"
my_last_name = "Doe"
my_full_name = my_first_name + " " + my_last_name
print(f"My full name: {my_full_name}")
print(f"Uppercase experiment: {my_full_name.upper()}")
print(f"Lowercase experiment: {my_full_name.lower()}")
print(f"Name length experiment: {len(my_full_name)}")

print("\n3. My User Input Experiment")
user_input = input("I'm going to enter my favorite color: ")
print(f"I entered: {user_input}")