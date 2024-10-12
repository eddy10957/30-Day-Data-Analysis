# control_structures.py - My experiments with Python control structures

# if/else statements
print("1. My if/else experiments")

my_age = 28
if my_age < 18:
    print("I'm a minor")
elif my_age >= 18 and my_age < 65:
    print("I'm an adult")
else:
    print("I'm a senior")

# Trying out a more complex condition
time = 14  # 24-hour format
if 5 <= time < 12:
    print("Good morning!")
elif 12 <= time < 18:
    print("Good afternoon!")
elif 18 <= time < 22:
    print("Good evening!")
else:
    print("Good night!")

print("\n2. My loop experiments")

# Testing a for loop with a list
my_favorite_foods = ["pizza", "sushi", "ice cream", "burger"]
print("My favorite foods:")
for food in my_favorite_foods:
    print(f"- {food}")

# Experimenting with range in a for loop
print("\nCounting from 1 to 5:")
for i in range(1, 6):
    print(i)

# Trying out a while loop
print("\nCountdown:")
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Blast off!")

# Combining loops and conditionals
print("\nEven numbers from 1 to 10:")
for num in range(1, 11):
    if num % 2 == 0:
        print(num)

# Experimenting with break and continue
print("\nLoop with break:")
for i in range(1, 11):
    if i == 5:
        break
    print(i)

print("\nLoop with continue:")
for i in range(1, 11):
    if i % 2 != 0:
        continue
    print(i)

# Create a simple number guessing game
print("\nMy number guessing game:")
import random
secret_number = random.randint(1, 10)
guess = 0
while guess != secret_number:
    guess = int(input("Guess the number (1-10): "))
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
print("You guessed it! The number was", secret_number)