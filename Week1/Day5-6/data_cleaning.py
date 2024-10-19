# data_cleaning.py - My exploration of data cleaning techniques

import pandas as pd
import numpy as np

# Create a sample dataset with various issues
data = {
    'name': ['John', 'Jane', 'Bob', 'Alice', np.nan, 'Charlie'],
    'age': [28, 34, np.nan, 31, 45, 'invalid'],
    'city': ['New York', 'paris', 'LONDON', 'Berlin', '', 'Chicago'],
    'salary': ['50000', '60000', '75000', '55000', 'N/A', '70000']
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

print("\n1. Handling missing values:")
# Drop rows with any missing values
df_dropped = df.dropna()
print("DataFrame with rows containing missing values dropped:")
print(df_dropped)

# Fill missing values
df['name'] = df['name'].fillna('Unknown')
df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Convert to numeric, invalid values become NaN
df['age'] = df['age'].fillna(df['age'].mean())
print("\nDataFrame with missing values filled:")
print(df)

print("\n2. Handling duplicates:")
# Add a duplicate row for demonstration
df = df.append(df.iloc[0], ignore_index=True)
print("DataFrame with a duplicate row:")
print(df)

# Remove duplicate rows
df_no_duplicates = df.drop_duplicates()
print("\nDataFrame with duplicates removed:")
print(df_no_duplicates)

print("\n3. Standardizing text data:")
# Convert city names to title case
df['city'] = df['city'].str.title()
print("Cities standardized to title case:")
print(df['city'])

print("\n4. Handling incorrect data types:")
# Convert salary to numeric, removing the 'N/A' first
df['salary'] = df['salary'].replace('N/A', np.nan)
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
print("\nSalary converted to numeric:")
print(df['salary'])

print("\n5. My custom experiment:")
# Create a new column 'experience' with some inconsistent data
df['experience'] = ['5 years', '7 years', '10 years', '3 years', 'entry level', '8 years', '5 years']

# Clean the 'experience' column
def clean_experience(exp):
    if isinstance(exp, str):
        if 'year' in exp:
            return int(exp.split()[0])
        elif exp == 'entry level':
            return 0
    return np.nan

df['experience_clean'] = df['experience'].apply(clean_experience)
print("\nCleaned 'experience' column:")
print(df[['experience', 'experience_clean']])

# Calculate correlation between age, salary, and experience
correlation = df[['age', 'salary', 'experience_clean']].corr()
print("\nCorrelation between age, salary, and experience:")
print(correlation)