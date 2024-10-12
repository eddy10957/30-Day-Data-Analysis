# file_operations.py - My experiments with Python file operations

# 1. Writing to a file
print("1. My file writing experiments")

# Writing a simple text file
with open('my_first_file.txt', 'w') as f:
    f.write("Hello, this is my first file operation!\n")
    f.write("I'm learning how to write to files in Python.\n")

print("I've written to 'my_first_file.txt'")

# Appending to the file
with open('my_first_file.txt', 'a') as f:
    f.write("This line is appended to the file.\n")

print("I've appended to 'my_first_file.txt'")

# 2. Reading from a file
print("\n2. My file reading experiments")

# Reading the entire file
print("Reading the entire file:")
with open('my_first_file.txt', 'r') as f:
    content = f.read()
    print(content)

# Reading line by line
print("\nReading line by line:")
with open('my_first_file.txt', 'r') as f:
    for line in f:
        print(line.strip())  # strip() removes the newline character

# 3. Working with CSV files
print("\n3. My CSV file experiments")

import csv

# Writing to a CSV file
with open('my_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Age', 'City'])
    writer.writerow(['Alice', 30, 'New York'])
    writer.writerow(['Bob', 25, 'Los Angeles'])
    writer.writerow(['Charlie', 35, 'Chicago'])

print("I've written data to 'my_data.csv'")

# Reading from a CSV file
print("\nReading from the CSV file:")
with open('my_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(', '.join(row))

# 4. Error handling in file operations
print("\n4. My error handling experiments")

try:
    with open('non_existent_file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("Oops! The file doesn't exist. I've handled this error gracefully.")

# 5. Word frequency counter
print("\n5. My word frequency counter challenge")

def word_frequency(filename):
    word_count = {}
    with open(filename, 'r') as f:
        for line in f:
            words = line.strip().lower().split()
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
    return word_count

# Count words in my_first_file.txt
freq = word_frequency('my_first_file.txt')
print("Word frequencies in 'my_first_file.txt':")
for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {count}")