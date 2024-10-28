# sql_basics.py - My first steps with SQLite and Python

import sqlite3
import pandas as pd
import numpy as np

# Create a connection to a new database
conn = sqlite3.connect('clinical_trials.db')
cursor = conn.cursor()

# Create tables for our clinical trials database
print("1. Creating database tables")

# Patients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    age INTEGER,
    sex TEXT,
    condition TEXT,
    enrollment_date DATE
)
''')

# Trials table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trials (
    trial_id TEXT PRIMARY KEY,
    treatment_name TEXT,
    start_date DATE,
    end_date DATE,
    phase INTEGER
)
''')

# Trial Results table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trial_results (
    result_id INTEGER PRIMARY KEY,
    patient_id TEXT,
    trial_id TEXT,
    treatment_response FLOAT,
    adverse_events INTEGER,
    completion_status TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (trial_id) REFERENCES trials (trial_id)
)
''')

# Generate some sample data
print("\n2. Generating sample data")

# Generate random patient data
np.random.seed(42)
patient_ids = [f'P{i:03d}' for i in range(1, 51)]
conditions = ['Type 1 Diabetes', 'Type 2 Diabetes', 'Hypertension']
enrollment_dates = pd.date_range('2023-01-01', '2023-12-31', periods=50)

patients_data = []
for i, patient_id in enumerate(patient_ids):
    patients_data.append((
        patient_id,
        np.random.randint(18, 75),
        np.random.choice(['M', 'F']),
        np.random.choice(conditions),
        enrollment_dates[i].strftime('%Y-%m-%d')
    ))

# Generate trial data
trial_ids = ['T001', 'T002', 'T003']
treatments = ['New Insulin Delivery', 'GLP-1 Analog', 'ACE Inhibitor']
start_dates = ['2023-01-15', '2023-02-01', '2023-03-01']
end_dates = ['2023-06-15', '2023-07-01', '2023-08-01']
phases = [2, 2, 3]

trials_data = list(zip(trial_ids, treatments, start_dates, end_dates, phases))

# Generate trial results
results_data = []
for i, patient_id in enumerate(patient_ids):
    trial_id = np.random.choice(trial_ids)
    results_data.append((
        i + 1,
        patient_id,
        trial_id,
        np.random.normal(0.65, 0.15),  # treatment response
        np.random.randint(0, 3),        # adverse events
        np.random.choice(['Completed', 'Withdrawn', 'Ongoing'], p=[0.8, 0.1, 0.1])
    ))

# Insert data into tables
print("3. Inserting data into tables")

cursor.executemany('INSERT OR REPLACE INTO patients VALUES (?,?,?,?,?)', patients_data)
cursor.executemany('INSERT OR REPLACE INTO trials VALUES (?,?,?,?,?)', trials_data)
cursor.executemany('INSERT OR REPLACE INTO trial_results VALUES (?,?,?,?,?,?)', results_data)

# Commit changes and close connection
conn.commit()

# Try some basic queries
print("\n4. Testing some basic queries")

print("\nNumber of patients per condition:")
cursor.execute('''
SELECT condition, COUNT(*) as patient_count 
FROM patients 
GROUP BY condition
''')
print(cursor.fetchall())

print("\nAverage treatment response by trial:")
cursor.execute('''
SELECT t.treatment_name, 
       AVG(tr.treatment_response) as avg_response,
       COUNT(*) as patient_count
FROM trials t
JOIN trial_results tr ON t.trial_id = tr.trial_id
GROUP BY t.treatment_name
''')
print(cursor.fetchall())

# Close connection
conn.close()

print("\nDatabase created and populated successfully!")
print("Check out 'clinical_trials.db' to see the database I created.")