# database_ops.py - My experiments with advanced database operations

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class ClinicalDatabaseManager:
    def __init__(self, db_name='clinical_trials.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.db_name}")
    
    def disconnect(self):
        """Safely disconnect from the database"""
        if self.conn:
            self.conn.close()
            print("Disconnected from database")
    
    def add_patient(self, patient_data):
        """Add a new patient to the database"""
        try:
            self.cursor.execute('''
                INSERT INTO patients (patient_id, age, sex, condition, enrollment_date)
                VALUES (?, ?, ?, ?, ?)
            ''', patient_data)
            self.conn.commit()
            print(f"Added patient {patient_data[0]}")
        except sqlite3.IntegrityError:
            print(f"Patient {patient_data[0]} already exists")
    
    def update_trial_result(self, result_id, new_response, new_status):
        """Update an existing trial result"""
        self.cursor.execute('''
            UPDATE trial_results
            SET treatment_response = ?, completion_status = ?
            WHERE result_id = ?
        ''', (new_response, new_status, result_id))
        self.conn.commit()
        print(f"Updated result {result_id}")
    
    def get_trial_summary(self, trial_id):
        """Get a summary of trial results"""
        self.cursor.execute('''
            SELECT 
                t.treatment_name,
                COUNT(*) as participants,
                AVG(tr.treatment_response) as avg_response,
                SUM(CASE WHEN tr.completion_status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM trials t
            JOIN trial_results tr ON t.trial_id = tr.trial_id
            WHERE t.trial_id = ?
            GROUP BY t.trial_id
        ''', (trial_id,))
        return self.cursor.fetchone()
    
    def export_to_csv(self, query, filename):
        """Export query results to CSV"""
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")

# Testing my database operations
print("1. Testing my database operations")
db = ClinicalDatabaseManager()
db.connect()

# Add a new patient
print("\n2. Adding a new patient")
new_patient = (
    'P051',
    45,
    'F',
    'Type 2 Diabetes',
    datetime.now().strftime('%Y-%m-%d')
)
db.add_patient(new_patient)

# Update a trial result
print("\n3. Updating a trial result")
db.update_trial_result(1, 0.85, 'Completed')

# Get trial summary
print("\n4. Getting trial summary")
summary = db.get_trial_summary('T001')
print("Trial Summary:", summary)

# Export data to CSV
print("\n5. Exporting trial results to CSV")
query = '''
    SELECT p.patient_id, p.age, p.condition, 
           t.treatment_name, tr.treatment_response
    FROM patients p
    JOIN trial_results tr ON p.patient_id = tr.patient_id
    JOIN trials t ON tr.trial_id = t.trial_id
'''
db.export_to_csv(query, 'trial_results_export.csv')

# Testing error handling
print("\n6. Testing error handling")
try:
    # Try to add a patient with existing ID
    db.add_patient(new_patient)
except sqlite3.IntegrityError as e:
    print(f"Caught expected error: {e}")

# Clean up
db.disconnect()