# linear_algebra_ops.py - My exploration of basic linear algebra operations

import numpy as np

# Creating sample matrices to experiment with
# np.array() creates a 2D array (matrix) from nested lists
A = np.array([[1, 2], [3, 4]])  # 2x2 matrix
B = np.array([[5, 6], [7, 8]])  # Another 2x2 matrix

print("My matrix A:")
print(A)
print("\nMy matrix B:")
print(B)

print("\nTrying matrix addition (A + B):")
# Matrix addition: adds corresponding elements
print(A + B)
# Takeaway: Matrix addition is element-wise and requires matrices of the same shape

print("\nAttempting matrix multiplication (A @ B):")
# @ operator performs matrix multiplication
print(A @ B)
# Takeaway: Matrix multiplication follows linear algebra rules:
# (m x n) matrix * (n x p) matrix = (m x p) matrix

print("\nExperimenting with element-wise multiplication (A * B):")
# * operator performs element-wise multiplication
print(A * B)
# Takeaway: This is different from matrix multiplication!
# It simply multiplies corresponding elements

print("\nFinding the transpose of A:")
# .T attribute gives the transpose of a matrix
print(A.T)
# Takeaway: Transposing switches rows and columns

print("\nCalculating the determinant of A:")
# np.linalg.det() computes the determinant of a square matrix
print(np.linalg.det(A))
# Takeaway: The determinant is a scalar value that provides information about the matrix
# (e.g., invertibility, scaling factor for area/volume)

print("\nComputing the inverse of A:")
# np.linalg.inv() computes the inverse of a square matrix
print(np.linalg.inv(A))
# Takeaway: Not all matrices have inverses (only square matrices with non-zero determinant)

print("\nFinding eigenvalues and eigenvectors of A:")
# np.linalg.eig() computes eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
# Takeaway: Eigenvalues and eigenvectors provide important information about linear transformations

print("\nSolving a linear equation Ax = b:")
b = np.array([1, 2])
# np.linalg.solve() solves the linear system Ax = b
x = np.linalg.solve(A, b)
print("Solution x:", x)
# Takeaway: This is equivalent to x = A^(-1) * b, but more numerically stable

print("\nMy custom experiment:")
# Create two 3x3 matrices with random integers
# np.random.randint(low, high, size) generates random integers
C = np.random.randint(1, 11, (3, 3))  # 3x3 matrix with integers from 1 to 10
D = np.random.randint(1, 11, (3, 3))  # Another 3x3 matrix

print("My matrix C:")
print(C)
print("\nMy matrix D:")
print(D)

print("\n1. Matrix addition of C and D:")
print(C + D)

print("\n2. Matrix multiplication of C and D:")
print(C @ D)

print("\n3. Determinant of C:")
print(np.linalg.det(C))

print("\n4. Inverse of D (if it exists):")
try:
    print(np.linalg.inv(D))
except np.linalg.LinAlgError:
    print("D is not invertible")
# Takeaway: Always check if a matrix is invertible before computing its inverse

print("\n5. Solving the equation Cx = b, where b is [1, 2, 3]:")
b = np.array([1, 2, 3])
try:
    # Attempt to solve the linear system
    x = np.linalg.solve(C, b)
    print("Solution x:", x)
except np.linalg.LinAlgError:
    print("This system doesn't have a unique solution")
# Takeaway: Not all systems of linear equations have solutions

# Overall takeaway: NumPy's linalg module provides powerful tools for linear algebra operations.
# These operations are fundamental in many areas of data science and machine learning,
# including data transformation, dimensionality reduction, and solving systems of equations.

# Key concepts introduced:
# 1. Matrix operations: addition, multiplication, element-wise multiplication
# 2. Transpose
# 3. Determinant
# 4. Matrix inverse
# 5. Eigenvalues and eigenvectors
# 6. Solving systems of linear equations