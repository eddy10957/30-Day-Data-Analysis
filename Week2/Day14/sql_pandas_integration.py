# sql_pandas_integration.py - Combining SQL and Pandas operations
# This script demonstrates how to effectively combine SQL and Pandas
# for clinical data analysis, showing best practices for each tool.

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import os

# Create visualization directory
visualization_path = os.path.join('..', '..', 'visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample clinical databases")

def create_clinical_database():
    """Create sample clinical database with multiple tables"""
    conn = sqlite3.connect('clinical_data.db')
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        age INTEGER,
        sex TEXT,
        enrollment_date DATE,
        study_site TEXT
    )
    ''')
    
    # Create lab_results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lab_results (
        result_id INTEGER PRIMARY KEY,
        patient_id TEXT,
        test_date DATE,
        test_name TEXT,
        value FLOAT,
        unit TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    )
    ''')
    
    # Create vital_signs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vital_signs (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        measurement_date DATE,
        heart_rate INTEGER,
        systolic_bp INTEGER,
        diastolic_bp INTEGER,
        temperature FLOAT,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    )
    ''')
    
    # Generate sample data
    np.random.seed(42)
    
    # Generate patient data
    patients = []
    sites = ['Site A', 'Site B', 'Site C']
    for i in range(100):
        patients.append((
            f'P{i:03d}',
            np.random.randint(18, 80),
            np.random.choice(['M', 'F']),
            (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
            np.random.choice(sites)
        ))
    
    # Insert patient data
    cursor.executemany(
        'INSERT OR REPLACE INTO patients VALUES (?, ?, ?, ?, ?)',
        patients
    )
    
    # Generate lab results
    lab_results = []
    test_types = ['Glucose', 'Cholesterol', 'Hemoglobin', 'Platelets']
    units = ['mg/dL', 'mg/dL', 'g/dL', 'K/µL']
    
    for i, (test, unit) in enumerate(zip(test_types, units)):
        for patient in patients:
            for _ in range(np.random.randint(1, 5)):
                lab_results.append((
                    None,
                    patient[0],
                    (datetime.strptime(patient[3], '%Y-%m-%d') + 
                     timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d'),
                    test,
                    np.random.normal(100, 15),
                    unit
                ))
    
    # Insert lab results
    cursor.executemany(
        'INSERT OR REPLACE INTO lab_results VALUES (?, ?, ?, ?, ?, ?)',
        lab_results
    )
    
    # Generate vital signs
    vital_signs = []
    for patient in patients:
        for _ in range(np.random.randint(2, 6)):
            vital_signs.append((
                patient[0],  # patient_id
                (datetime.strptime(patient[3], '%Y-%m-%d') + 
                 timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d'),
                np.random.randint(60, 100),  # heart_rate
                np.random.randint(110, 140),  # systolic_bp
                np.random.randint(60, 90),    # diastolic_bp
                np.random.normal(37, 0.3)     # temperature
            ))
    
    # Insert vital signs
    cursor.executemany(
        '''INSERT OR REPLACE INTO vital_signs 
           (patient_id, measurement_date, heart_rate, systolic_bp, 
            diastolic_bp, temperature) 
           VALUES (?, ?, ?, ?, ?, ?)''',
        vital_signs
    )
    
    conn.commit()
    return conn

# Create database
conn = create_clinical_database()

print("\n2. Demonstrating SQL queries with Pandas")

# Basic query using Pandas
query = '''
SELECT p.patient_id, p.age, p.sex, 
       COUNT(DISTINCT l.result_id) as lab_count,
       COUNT(DISTINCT v.measurement_date) as vitals_count
FROM patients p
LEFT JOIN lab_results l ON p.patient_id = l.patient_id
LEFT JOIN vital_signs v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.age, p.sex
'''

patient_summary = pd.read_sql_query(query, conn)
print("\nPatient summary:")
print(patient_summary.head())

print("\n3. Combining SQL and Pandas operations")

# Get lab results for analysis
lab_data = pd.read_sql_query('''
SELECT p.patient_id, p.age, p.sex, p.study_site,
       l.test_name, l.value, l.unit, l.test_date
FROM patients p
JOIN lab_results l ON p.patient_id = l.patient_id
''', conn)

# Perform Pandas operations
lab_stats = lab_data.groupby(['test_name', 'study_site']).agg({
    'value': ['count', 'mean', 'std'],
    'patient_id': 'nunique'
}).round(2)

print("\nLab statistics by test and site:")
print(lab_stats)

print("\n4. Advanced integration example")

def analyze_patient_trends():
    """Combine SQL and Pandas for trend analysis"""
    
    # Get vital signs with SQL
    vitals_query = '''
    SELECT p.patient_id, p.age, p.sex, p.study_site,
           v.measurement_date, v.heart_rate, 
           v.systolic_bp, v.diastolic_bp
    FROM patients p
    JOIN vital_signs v ON p.patient_id = v.patient_id
    ORDER BY p.patient_id, v.measurement_date
    '''
    
    vitals_df = pd.read_sql_query(vitals_query, conn)
    
    # Convert date string to datetime
    vitals_df['measurement_date'] = pd.to_datetime(vitals_df['measurement_date'])
    
    # Calculate trends using Pandas
    trends = vitals_df.groupby('patient_id').agg({
        'heart_rate': ['mean', 'std', 'count'],
        'systolic_bp': ['mean', 'std'],
        'diastolic_bp': ['mean', 'std']
    }).round(2)
    
    return trends

patient_trends = analyze_patient_trends()
print("\nPatient vital signs trends:")
print(patient_trends.head())

print("\n5. Writing results back to database")

# Create a new table for analysis results with correct column names
cursor = conn.cursor()
cursor.execute('''
DROP TABLE IF EXISTS analysis_results
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS analysis_results (
    patient_id TEXT PRIMARY KEY,
    heart_rate_mean FLOAT,
    heart_rate_std FLOAT,
    heart_rate_count INTEGER,
    systolic_bp_mean FLOAT,
    systolic_bp_std FLOAT,
    diastolic_bp_mean FLOAT,
    diastolic_bp_std FLOAT
)
''')

# Prepare results for SQL
analysis_results = patient_trends.reset_index()
analysis_results.columns = ['patient_id', 'heart_rate_mean', 'heart_rate_std', 'heart_rate_count',
                          'systolic_bp_mean', 'systolic_bp_std', 'diastolic_bp_mean', 'diastolic_bp_std']

# Write results back to SQLite
analysis_results.to_sql('analysis_results', conn, if_exists='replace', index=False)

print("\n6. Verifying results")

# Update final query to use correct column names
final_query = '''
SELECT p.patient_id, p.age, p.sex, p.study_site,
       a.heart_rate_mean, a.systolic_bp_mean, a.heart_rate_count
FROM patients p
JOIN analysis_results a ON p.patient_id = a.patient_id
WHERE a.heart_rate_count >= 3
ORDER BY a.heart_rate_mean DESC
LIMIT 5
'''

final_results = pd.read_sql_query(final_query, conn)
print("\nTop 5 patients by average heart rate (with ≥3 measurements):")
print(final_results)

# Close connection
conn.close()

print("\nIntegration complete! Database 'clinical_data.db' contains all results.")