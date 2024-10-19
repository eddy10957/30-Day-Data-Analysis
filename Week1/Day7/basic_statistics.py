# basic_statistics.py - Applying statistical concepts and reviewing week's learning

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Create a sample dataset
np.random.seed(42)
data = np.random.normal(loc=100, scale=20, size=1000)
df = pd.DataFrame(data, columns=['value'])

print("1. Measures of Central Tendency")
print(f"Mean: {np.mean(data):.2f}")
print(f"Median: {np.median(data):.2f}")

# Mode calculation handling both scalar and array outputs
mode_result = stats.mode(data)
mode_value = mode_result.mode
if np.isscalar(mode_value):
    print(f"Mode: {mode_value:.2f}")
else:
    print(f"Mode: {mode_value[0]:.2f}")

print("\n2. Measures of Dispersion")
print(f"Variance: {np.var(data):.2f}")
print(f"Standard Deviation: {np.std(data):.2f}")
print(f"Range: {np.ptp(data):.2f}")


print("\n3. Data Visualization")
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, edgecolor='black')
plt.title('Distribution of Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.savefig('data_distribution.png')
plt.close()

print("Histogram saved as 'data_distribution.png'")

print("\n4. Probability Distributions")
# Generate data from different distributions
normal_data = np.random.normal(loc=0, scale=1, size=1000)
uniform_data = np.random.uniform(low=-3, high=3, size=1000)
exponential_data = np.random.exponential(scale=1, size=1000)

plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.hist(normal_data, bins=30, edgecolor='black')
plt.title('Normal Distribution')
plt.subplot(132)
plt.hist(uniform_data, bins=30, edgecolor='black')
plt.title('Uniform Distribution')
plt.subplot(133)
plt.hist(exponential_data, bins=30, edgecolor='black')
plt.title('Exponential Distribution')
plt.tight_layout()
plt.savefig('probability_distributions.png')
plt.close()

print("Probability distributions saved as 'probability_distributions.png'")

print("\n5. Correlation and Covariance")
# Create two correlated variables
x = np.random.normal(0, 1, 1000)
y = x + np.random.normal(0, 0.5, 1000)  # y is correlated with x

print(f"Correlation between x and y: {np.corrcoef(x, y)[0, 1]:.2f}")
print(f"Covariance between x and y: {np.cov(x, y)[0, 1]:.2f}")

plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.5)
plt.title('Scatter plot of correlated variables')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('correlation_plot.png')
plt.close()

print("Correlation plot saved as 'correlation_plot.png'")

print("\n6. Week 1 Review: Applying Concepts")

# Create a DataFrame with random sales data
dates = pd.date_range('2023-01-01', periods=100)
sales_data = pd.DataFrame({
    'date': dates,
    'product_a': np.random.randint(50, 200, 100),
    'product_b': np.random.randint(30, 150, 100)
})

print("Sample of sales data:")
print(sales_data.head())

# Basic statistics
print("\nDescriptive statistics of sales data:")
print(sales_data.describe())

# Data manipulation
sales_data['total_sales'] = sales_data['product_a'] + sales_data['product_b']
sales_data['sales_diff'] = sales_data['product_a'] - sales_data['product_b']

# Time series analysis
monthly_sales = sales_data.resample('M', on='date').sum()
print("\nMonthly sales:")
print(monthly_sales)

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(sales_data['date'], sales_data['product_a'], label='Product A')
plt.plot(sales_data['date'], sales_data['product_b'], label='Product B')
plt.title('Daily Sales of Products A and B')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.savefig('sales_time_series.png')
plt.close()

print("Sales time series plot saved as 'sales_time_series.png'")

# Correlation analysis
correlation = sales_data[['product_a', 'product_b']].corr()
print("\nCorrelation between product A and B sales:")
print(correlation)

print("\nWeek 1 learning applied to analyze sales data!")