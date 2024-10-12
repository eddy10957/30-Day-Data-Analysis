# functions_and_modules.py - My experiments with Python functions and modules

# [The content remains the same as in the previous version up to the module experiments]

# 4. Working with modules
print("\n4. My module experiments")

# Built-in modules
import random
print(f"Random number between 1 and 10: {random.randint(1, 10)}")

from math import pi, sqrt
print(f"Square root of 16: {sqrt(16)}")
print(f"Value of pi: {pi}")

# Using my own module
import my_math

print(f"5 + 3 = {my_math.add(5, 3)}")
print(f"10 - 4 = {my_math.subtract(10, 4)}")

# 5. My challenge: Using a simple calculator module
import calculator

print("\n5. My calculator module challenge")
print(f"2 + 3 = {calculator.add(2, 3)}")
print(f"5 * 4 = {calculator.multiply(5, 4)}")
print(f"10 / 3 = {calculator.divide(10, 3)}")
