# pandas_basics.py - My experiments with Pandas Series and DataFrames

import pandas as pd
import numpy as np

print("1. Creating and working with Series:")
# Create a Series from a list
my_series = pd.Series([1, 3, 5, np.nan, 6, 8])
print(my_series)

# Create a Series with custom index
my_series_2 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
print("\nSeries with custom index:")
print(my_series_2)

print("\n2. Creating and working with DataFrames:")
# Create a DataFrame from a dictionary
data = {'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [28, 34, 42, 31],
        'city': ['New York', 'Paris', 'London', 'Berlin']}
df = pd.DataFrame(data)
print(df)

# Create a DataFrame with a DatetimeIndex
dates = pd.date_range('20230101', periods=6)
df_2 = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print("\nDataFrame with DatetimeIndex:")
print(df_2)

print("\n3. Basic DataFrame operations:")
# Display basic information about the DataFrame
print(df.info())

# Display summary statistics
print("\nSummary statistics:")
print(df.describe())

# Select a single column
print("\nSelecting the 'name' column:")
print(df['name'])

# Select multiple columns
print("\nSelecting 'name' and 'age' columns:")
print(df[['name', 'age']])

# Select rows by label (index)
print("\nSelecting rows by index:")
print(df_2.loc['2023-01-02':'2023-01-04'])

# Select rows by integer position
print("\nSelecting rows by integer position:")
print(df.iloc[1:3])

print("\n4. My custom experiment:")
# Create a DataFrame with some missing values
data_2 = {'A': [1, 2, np.nan, 4],
          'B': [5, np.nan, np.nan, 8],
          'C': [9, 10, 11, 12]}
df_3 = pd.DataFrame(data_2)
print("DataFrame with missing values:")
print(df_3)

# Fill missing values with the mean of each column
df_3_filled = df_3.fillna(df_3.mean())
print("\nDataFrame with missing values filled:")
print(df_3_filled)

# Perform some calculations
print("\nSum of each column:")
print(df_3_filled.sum())

print("\nMean of each column:")
print(df_3_filled.mean())

# Group by a column and perform aggregation
df_4 = pd.DataFrame({'category': ['A', 'B', 'A', 'B', 'A', 'B'],
                     'value': [1, 2, 3, 4, 5, 6]})
print("\nGrouping and aggregation:")
print(df_4.groupby('category').agg({'value': ['mean', 'sum']}))
