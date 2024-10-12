# sales_analysis.py - Applying NumPy to analyze sales data

import numpy as np

# 1. Generate sample sales data
np.random.seed(42)  # for reproducibility

# Generate data for 12 months and 5 products
months = 12
products = 5

# Create a 2D array of sales data: rows are months, columns are products
sales_data = np.random.randint(100, 1000, size=(months, products))

print("Sample sales data (rows: months, columns: products):")
print(sales_data)

# 2. Perform basic statistical analysis
print("\nBasic statistical analysis:")
print(f"Total sales: {np.sum(sales_data)}")
print(f"Average monthly sales: {np.mean(sales_data)}")
print(f"Highest monthly sales: {np.max(sales_data)}")
print(f"Lowest monthly sales: {np.min(sales_data)}")

# 3. Calculate monthly and product-wise totals
monthly_totals = np.sum(sales_data, axis=1)
product_totals = np.sum(sales_data, axis=0)

print("\nMonthly sales totals:")
print(monthly_totals)

print("\nProduct-wise sales totals:")
print(product_totals)

# 4. Find the best-selling product for each month
best_selling_products = np.argmax(sales_data, axis=1)
print("\nBest-selling product for each month (0-indexed):")
print(best_selling_products)

# 5. Calculate the percentage of sales for each product
product_percentages = (product_totals / np.sum(sales_data)) * 100
print("\nPercentage of sales for each product:")
print(product_percentages)

# 6. Find months with above-average sales
average_sales = np.mean(sales_data)
above_average_months = np.where(monthly_totals > average_sales)[0]
print("\nMonths with above-average sales (0-indexed):")
print(above_average_months)

# 7. Calculate the correlation between products
correlation_matrix = np.corrcoef(sales_data.T)
print("\nCorrelation matrix between products:")
print(correlation_matrix)

# 8. Predict next month's sales (simple moving average)
last_3_months = sales_data[-3:, :]
next_month_prediction = np.mean(last_3_months, axis=0)
print("\nPredicted sales for next month (simple moving average):")
print(next_month_prediction)