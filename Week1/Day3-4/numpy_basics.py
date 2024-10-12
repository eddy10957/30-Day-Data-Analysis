# numpy_basics.py - My experiments with NumPy arrays and operations

import numpy as np  # Import NumPy, conventionally aliased as 'np'

print("My NumPy Array Creation Experiments:")
# np.array() converts a Python list into a NumPy array
# Input: A Python list (or nested list for multi-dimensional arrays)
my_first_array = np.array([1, 2, 3, 4, 5])
print("1D array:", my_first_array)
# Takeaway: np.array() can create arrays from Python lists

# For 2D arrays, we use nested lists
my_2d_array = np.array([[1, 2, 3], [4, 5, 6]])
print("2D array:\n", my_2d_array)
# Takeaway: The shape of the array is determined by the structure of the input list

print("\nLearning about array attributes:")
# shape is a tuple representing the dimensions of the array
print("Shape of my_2d_array:", my_2d_array.shape)
# ndim gives the number of dimensions (1 for 1D, 2 for 2D, etc.)
print("Dimensions of my_2d_array:", my_2d_array.ndim)
# dtype shows the data type of the array elements
print("Data type of my_2d_array:", my_2d_array.dtype)
# Takeaway: These attributes provide important information about the array's structure

print("\nTrying out array creation functions:")
# np.zeros() creates an array filled with zeros
# Input: A tuple representing the shape of the array
my_zeros = np.zeros((3, 3))  # Creates a 3x3 array of zeros
print("Zeros array:\n", my_zeros)

# np.ones() creates an array filled with ones
my_ones = np.ones((2, 4))  # Creates a 2x4 array of ones
print("Ones array:\n", my_ones)

# np.arange() creates an array with evenly spaced values within a given interval
# Inputs: start, stop, step (similar to Python's range())
my_range = np.arange(0, 10, 2)  # Creates array [0, 2, 4, 6, 8]
print("Arange array:", my_range)

# np.linspace() creates an array with evenly spaced numbers over a specified interval
# Inputs: start, stop, num (number of elements)
my_linspace = np.linspace(0, 1, 5)  # Creates 5 evenly spaced numbers between 0 and 1
print("Linspace array:", my_linspace)
# Takeaway: NumPy provides various functions to create arrays with specific patterns

print("\nExperimenting with basic array operations:")
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# NumPy performs element-wise operations on arrays
print("Addition:", arr1 + arr2)      # Adds corresponding elements
print("Multiplication:", arr1 * arr2)  # Multiplies corresponding elements
print("Division:", arr2 / arr1)      # Divides corresponding elements
# Takeaway: These operations are performed element-wise, not like matrix operations

print("\nTrying out universal functions (ufuncs):")
# ufuncs operate element-wise on arrays
print("Square root:", np.sqrt(arr1))  # Takes square root of each element
print("Exponential:", np.exp(arr1))   # e raised to the power of each element
# Takeaway: ufuncs provide fast element-wise operations on arrays

print("\nMy custom experiment:")
# np.random.randint() generates random integers
# Inputs: low (inclusive), high (exclusive), size (shape of output)
my_random_array = np.random.randint(1, 11, (3, 3))  # 3x3 array of random ints from 1 to 10
print("My random array:\n", my_random_array)

# NumPy provides functions for basic statistical operations
print("Mean:", np.mean(my_random_array))  # Average of all elements
print("Median:", np.median(my_random_array))  # Middle value when elements are sorted
print("Standard deviation:", np.std(my_random_array))  # Measure of spread of values
# Takeaway: NumPy includes many statistical functions that operate on entire arrays

# Overall takeaway: NumPy provides powerful tools for creating, manipulating,
# and analyzing numerical data in Python. Its array operations are efficient
# and easy to use, making it essential for data analysis and scientific computing.