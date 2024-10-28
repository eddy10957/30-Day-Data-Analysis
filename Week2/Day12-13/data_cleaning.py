# data_cleaning.py - Basic data cleaning operations on clinical data
# This script demonstrates common data cleaning techniques using a synthetic clinical dataset,
# showing how to handle real-world data issues often encountered in medical research.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import os

# Create visualization directory
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample messy clinical data")

# Generate synthetic messy clinical trial data
np.random.seed(42)

def create_messy_clinical_data(n_patients=100):
    """
    Create synthetic clinical data with common real-world issues:
    - Inconsistent date formats
    - Mixed case text
    - Typos in categorical variables
    - Invalid numerical values
    - Missing data
    - Inconsistent units
    """
    patients = []
    
    for i in range(n_patients):
        # Create base patient record
        patient = {
            'patient_id': f'PT{i:03d}',
            'age': np.random.randint(18, 90),
            'sex': np.random.choice(['M', 'F', 'm', 'f', 'Male', 'Female']),
            'weight': np.random.normal(70, 15),  # Weight in kg
            'height': np.random.normal(170, 20),  # Height in cm
        }
        
        # Add some weights in pounds instead of kg (inconsistent units)
        if np.random.random() < 0.2:
            patient['weight'] *= 2.20462  # Convert to pounds
            
        # Add enrollment dates with inconsistent formats
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%b-%Y']
        base_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        patient['enrollment_date'] = base_date.strftime(np.random.choice(date_formats))
        
        # Add disease type with typos and inconsistent capitalization
        diseases = ['Diabetes Type 2', 'diabetes type 2', 'DiabetesT2', 'type 2 diabetes',
                   'Hypertension', 'hypertension', 'HTN', 'HyperTension']
        patient['disease'] = np.random.choice(diseases)
        
        # Add lab results with some invalid values
        patient['glucose_level'] = np.random.normal(130, 20)
        if np.random.random() < 0.1:  # 10% invalid values
            patient['glucose_level'] = np.random.choice([-999, 0, 9999])
            
        # Add some missing values
        if np.random.random() < 0.1:  # 10% missing rate
            for field in ['weight', 'height', 'glucose_level']:
                patient[field] = np.random.choice([np.nan, None])  # Only use proper missing value indicators
                
        patients.append(patient)
    
    return pd.DataFrame(patients)

# Create our messy dataset
df = create_messy_clinical_data(200)
print("\nOriginal messy data:")
print(df.head())
print("\nData info:")
print(df.info())

print("\n2. Basic cleaning operations")

def clean_basic(df):
    """Perform basic cleaning operations on the dataset"""
    # Create a copy to avoid modifying the original data
    cleaned = df.copy()
    
    # Standardize patient sex
    sex_mapping = {
        'M': 'Male', 'm': 'Male', 'Male': 'Male',
        'F': 'Female', 'f': 'Female', 'Female': 'Female'
    }
    cleaned['sex'] = cleaned['sex'].map(sex_mapping)
    
    # Clean disease names
    def standardize_disease(disease):
        disease = str(disease).lower().strip()
        if 'diabetes' in disease or 'diabet' in disease:
            return 'Diabetes Type 2'
        elif any(x in disease for x in ['hypertension', 'htn']):
            return 'Hypertension'
        return disease
    
    cleaned['disease'] = cleaned['disease'].apply(standardize_disease)
    
    # Convert weight to numeric, handling any string values first
    cleaned['weight'] = pd.to_numeric(cleaned['weight'], errors='coerce')
    
    # Convert all weights to kg if they appear to be in pounds (over 120)
    likely_pounds = cleaned['weight'] > 120
    cleaned.loc[likely_pounds, 'weight'] = cleaned.loc[likely_pounds, 'weight'] / 2.20462
    
    return cleaned

cleaned_df = clean_basic(df)
print("\nAfter basic cleaning:")
print(cleaned_df.head())

print("\n3. Handling dates")

def clean_dates(df):
    """Standardize date formats"""
    def parse_date(date_str):
        """Try multiple date formats"""
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%b-%Y']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        return pd.NaT
    
    df['enrollment_date'] = df['enrollment_date'].apply(parse_date)
    return df

cleaned_df = clean_dates(cleaned_df)
print("\nAfter date cleaning:")
print(cleaned_df['enrollment_date'].head())

print("\n4. Handling missing values")

def handle_missing_values(df):
    """Handle missing values appropriately for each column"""
    df = df.copy()
    
    # Check missing value patterns
    missing_summary = pd.DataFrame({
        'percent_missing': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print("\nMissing value summary:")
    print(missing_summary)
    
    # Replace empty strings and 'missing' with NaN
    df = df.replace(['', 'missing'], np.nan)
    
    # Handle missing values based on column type
    # Numeric columns: fill with median
    df['weight'].fillna(df['weight'].median(), inplace=True)
    df['height'].fillna(df['height'].median(), inplace=True)
    df['glucose_level'].fillna(df['glucose_level'].median(), inplace=True)
    
    # Categorical columns: fill with mode
    df['sex'].fillna(df['sex'].mode()[0], inplace=True)
    df['disease'].fillna(df['disease'].mode()[0], inplace=True)
    
    return df

cleaned_df = handle_missing_values(cleaned_df)
print("\nAfter handling missing values:")
print(cleaned_df.isnull().sum())

print("\n5. Handling invalid values")

def handle_invalid_values(df):
    """Clean invalid values from numeric columns"""
    df = df.copy()
    
    # Define valid ranges for each measurement
    valid_ranges = {
        'age': (0, 120),
        'weight': (20, 200),  # kg
        'height': (100, 220),  # cm
        'glucose_level': (30, 500)  # mg/dL
    }
    
    # Replace out-of-range values with NaN and then fill
    for column, (min_val, max_val) in valid_ranges.items():
        mask = (df[column] < min_val) | (df[column] > max_val)
        df.loc[mask, column] = np.nan
        df[column].fillna(df[column].median(), inplace=True)
    
    return df

cleaned_df = handle_invalid_values(cleaned_df)
print("\nAfter handling invalid values:")
print(cleaned_df.describe())

print("\n6. Adding derived features")

def add_derived_features(df):
    """Create new features from existing data"""
    df = df.copy()
    
    # Calculate BMI
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], 
                            bins=[0, 30, 50, 70, 100],
                            labels=['<30', '30-50', '50-70', '>70'])
    
    # Calculate days since enrollment
    df['days_since_enrollment'] = (pd.Timestamp.now() - df['enrollment_date']).dt.days
    
    return df

cleaned_df = add_derived_features(cleaned_df)
print("\nAfter adding derived features:")
print(cleaned_df.head())

print("\n7. Final validation")

def validate_cleaned_data(df):
    """Perform final validation checks on cleaned data"""
    validation_results = {
        'no_missing_values': df.isnull().sum().sum() == 0,
        'valid_bmi_range': (df['bmi'] >= 15).all() and (df['bmi'] <= 50).all(),
        'valid_sex_categories': df['sex'].isin(['Male', 'Female']).all(),
        'valid_dates': df['enrollment_date'].notna().all(),
    }
    
    print("\nValidation results:")
    for check, result in validation_results.items():
        print(f"{check}: {'✓' if result else '✗'}")
    
    return all(validation_results.values())

is_valid = validate_cleaned_data(cleaned_df)

# Export cleaned data
output_dir = 'cleaned_data'
os.makedirs(output_dir, exist_ok=True)
cleaned_df.to_csv(os.path.join(output_dir, 'cleaned_clinical_data.csv'), index=False)

print("\nCleaning complete! Check 'cleaned_data' directory for the cleaned dataset.")