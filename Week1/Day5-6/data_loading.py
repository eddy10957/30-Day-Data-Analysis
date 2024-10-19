# data_loading.py - My practice with loading data from different sources

import pandas as pd
import numpy as np
import io

print("1. Loading data from CSV:")
# Create a sample CSV string (in real scenarios, this would be a file)
csv_data = """
name,age,city
John,28,New York
Jane,34,Paris
Bob,42,London
Alice,31,Berlin
"""
df_csv = pd.read_csv(io.StringIO(csv_data))
print(df_csv)

print("\n2. Loading data from JSON:")
# Create a sample JSON string
json_data = """
[
  {"name": "John", "age": 28, "city": "New York"},
  {"name": "Jane", "age": 34, "city": "Paris"},
  {"name": "Bob", "age": 42, "city": "London"},
  {"name": "Alice", "age": 31, "city": "Berlin"}
]
"""
df_json = pd.read_json(io.StringIO(json_data))
print(df_json)

print("\n3. Loading data from Excel:")
# Note: In a real scenario, I'd use pd.read_excel('filename.xlsx')
# For this example, I'll create a DataFrame and save it to Excel
df_excel = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [28, 34, 42, 31],
    'city': ['New York', 'Paris', 'London', 'Berlin']
})
df_excel.to_excel('sample.xlsx', index=False)
df_excel_loaded = pd.read_excel('sample.xlsx')
print(df_excel_loaded)

print("\n4. Loading data from a dictionary:")
data_dict = {
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [28, 34, 42, 31],
    'city': ['New York', 'Paris', 'London', 'Berlin']
}
df_dict = pd.DataFrame(data_dict)
print(df_dict)

print("\n5. Loading data from a list of lists:")
data_list = [
    ['John', 28, 'New York'],
    ['Jane', 34, 'Paris'],
    ['Bob', 42, 'London'],
    ['Alice', 31, 'Berlin']
]
df_list = pd.DataFrame(data_list, columns=['name', 'age', 'city'])
print(df_list)

print("\n6. My custom experiment:")
# Create a more complex dataset
data = {
    'date': pd.date_range(start='2023-01-01', periods=10),
    'category': np.random.choice(['A', 'B', 'C'], 10),
    'value': np.random.randn(10),
    'is_valid': np.random.choice([True, False], 10)
}
df_complex = pd.DataFrame(data)
print(df_complex)

# Save to CSV
df_complex.to_csv('complex_data.csv', index=False)

# Read back from CSV, specifying dtypes
df_loaded = pd.read_csv('complex_data.csv', 
                        parse_dates=['date'],
                        dtype={'category': 'category', 'is_valid': bool})
print("\nLoaded data with specified dtypes:")
print(df_loaded.dtypes)
