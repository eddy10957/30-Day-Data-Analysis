# array_indexing_slicing.py - My practice with array indexing and slicing

import numpy as np

# Creating a sample 2D array to experiment with
# np.array() takes a list (or nested list for 2D) as input
my_array = np.array([[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12]])

print("My experimental array:")
print(my_array)

print("\nTrying out indexing:")
# my_array[row, column] accesses a specific element
print("Element at position (1, 2):", my_array[1, 2])
# my_array[row] accesses an entire row
print("First row:", my_array[0])
# Takeaway: NumPy arrays use zero-based indexing, like Python lists

print("\nExperimenting with slicing:")
# The colon ':' is used for slicing. It means "all elements along this axis"
# my_array[start:end, start:end] - The end index is exclusive
print("First two rows, all columns:")
print(my_array[:2, :])  # :2 means "from the start up to (but not including) index 2"
                        # : alone means "all elements"

# Negative indices count from the end of the array
print("\nAll rows, last two columns:")
print(my_array[:, -2:])  # : means "all rows", -2: means "from the second-to-last to the end"
# Takeaway: Slicing allows you to extract subarrays easily

print("\nAttempting boolean indexing:")
# Create a boolean mask: True where condition is met, False otherwise
bool_idx = my_array > 5
print("Elements greater than 5:")
print(my_array[bool_idx])  # Only elements where bool_idx is True are selected
# Takeaway: Boolean indexing allows you to select elements based on conditions

print("\nExploring fancy indexing:")
# np.array() is used here to create arrays of indices
row_indices = np.array([0, 2])
col_indices = np.array([1, 3])
print("Selected elements:")
# np.newaxis is used to increase the dimension of row_indices
# This allows broadcasting to work correctly with col_indices
print(my_array[row_indices[:, np.newaxis], col_indices])
# Takeaway: Fancy indexing allows you to select multiple elements at once using integer arrays

print("\nMy custom experiment:")
# np.arange(start, stop) creates an array of integers from start to stop-1
# reshape(rows, cols) reshapes the 1D array into a 2D array
my_custom_array = np.arange(1, 26).reshape(5, 5)
print("My 5x5 array:")
print(my_custom_array)

print("\n1. Element at position (2, 3):", my_custom_array[2, 3])
print("2. Second row:", my_custom_array[1])  # Remember, zero-based indexing
print("3. Last two columns:\n", my_custom_array[:, -2:])
print("4. All elements greater than 15:", my_custom_array[my_custom_array > 15])
print("5. Elements at positions (0,0), (2,2), and (4,4):")
# Using lists for fancy indexing
print(my_custom_array[[0, 2, 4], [0, 2, 4]])

# Overall takeaway: NumPy provides powerful and flexible ways to access and
# manipulate array elements. Understanding indexing and slicing syntax is
# crucial for efficient data manipulation in data analysis tasks.