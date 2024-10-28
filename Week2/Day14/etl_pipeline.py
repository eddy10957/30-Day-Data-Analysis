# etl_pipeline.py - Building an ETL pipeline for clinical data
# This script demonstrates a complete Extract, Transform, Load pipeline,
# showing how to process clinical data from multiple sources to final analysis.

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import os
import json
from pathlib import Path

class ClinicalDataETL:
    def __init__(self):
        """Initialize ETL pipeline with necessary paths and connections"""
        # Set up paths
        self.base_path = Path('data')
        self.raw_path = self.base_path / 'raw'
        self.processed_path = self.base_path / 'processed'
        self.output_path = self.base_path / 'output'
        
        # Create directories if they don't exist
        for path in [self.base_path, self.raw_path, self.processed_path, self.output_path]:
            path.mkdir(exist_ok=True)
        
        # Initialize database connection
        self.db_path = 'clinical_data.db'
        
        # Set up logging
        self.log = []
    
    def extract_data(self):
        """
        Extract data from multiple sources:
        1. CSV files (lab results)
        2. JSON files (patient info)
        3. SQLite database (vital signs)
        """
        print("1. Extracting data from multiple sources")
        
        # Generate sample data for demonstration
        self._generate_sample_data()
        
        # Read lab results from CSV
        lab_results = pd.read_csv(self.raw_path / 'lab_results.csv')
        
        # Read patient info from JSON
        with open(self.raw_path / 'patient_info.json', 'r') as f:
            patient_info = pd.DataFrame(json.load(f))
        
        # Read vital signs from SQLite
        conn = sqlite3.connect(self.db_path)
        vitals = pd.read_sql('SELECT * FROM vital_signs', conn)
        conn.close()
        
        self.log.append(f"Extracted {len(lab_results)} lab results")
        self.log.append(f"Extracted {len(patient_info)} patient records")
        self.log.append(f"Extracted {len(vitals)} vital sign measurements")
        
        return lab_results, patient_info, vitals
    
    def transform_data(self, lab_results, patient_info, vitals):
        """
        Transform and clean the data:
        1. Handle missing values
        2. Standardize formats
        3. Create derived features
        4. Validate data quality
        """
        print("\n2. Transforming and cleaning data")
        
        # Clean patient information
        patient_info_clean = self._clean_patient_data(patient_info)
        
        # Clean and standardize lab results
        lab_results_clean = self._clean_lab_results(lab_results)
        
        # Clean vital signs
        vitals_clean = self._clean_vital_signs(vitals)
        
        # Create derived features
        enriched_data = self._create_derived_features(
            patient_info_clean, lab_results_clean, vitals_clean)
        
        return enriched_data
    
    def load_data(self, enriched_data):
        """
        Load processed data:
        1. Save to database
        2. Export analysis files
        3. Generate reports
        """
        print("\n3. Loading processed data")
        
        # Save to SQLite database
        conn = sqlite3.connect(self.db_path)
        
        # Save different aspects of the enriched data
        for table_name, data in enriched_data.items():
            data.to_sql(f'processed_{table_name}', conn, if_exists='replace', index=False)
            self.log.append(f"Saved {len(data)} records to processed_{table_name}")
        
        conn.close()
        
        # Export CSV files
        for table_name, data in enriched_data.items():
            output_file = self.output_path / f'{table_name}_processed.csv'
            data.to_csv(output_file, index=False)
            self.log.append(f"Exported {table_name} to {output_file}")
        
        # Generate summary report
        self._generate_summary_report(enriched_data)
    
    def _generate_sample_data(self):
        """Generate sample data files for demonstration"""
        np.random.seed(42)
        
        # Generate lab results
        lab_results = []
        for i in range(100):
            for _ in range(np.random.randint(2, 6)):
                lab_results.append({
                    'patient_id': f'P{i:03d}',
                    'test_date': (datetime.now() - timedelta(days=np.random.randint(0, 180))).strftime('%Y-%m-%d'),
                    'test_name': np.random.choice(['Glucose', 'Hemoglobin', 'Platelets']),
                    'value': np.random.normal(100, 15),
                    'unit': np.random.choice(['mg/dL', 'g/dL', 'K/µL'])
                })
        
        pd.DataFrame(lab_results).to_csv(self.raw_path / 'lab_results.csv', index=False)
        
        # Generate patient info
        patients = []
        for i in range(100):
            patients.append({
                'patient_id': f'P{i:03d}',
                'age': np.random.randint(18, 80),
                'sex': np.random.choice(['M', 'F']),
                'diagnosis': np.random.choice(['Type 1 Diabetes', 'Type 2 Diabetes', 'Hypertension']),
                'enrollment_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
            })
        
        with open(self.raw_path / 'patient_info.json', 'w') as f:
            json.dump(patients, f)
        
        # Generate vital signs in SQLite
        conn = sqlite3.connect(self.db_path)
        vitals = []
        for i in range(100):
            for _ in range(np.random.randint(3, 8)):
                vitals.append({
                    'patient_id': f'P{i:03d}',
                    'measurement_date': (datetime.now() - timedelta(days=np.random.randint(0, 180))).strftime('%Y-%m-%d'),
                    'systolic_bp': np.random.randint(110, 140),
                    'diastolic_bp': np.random.randint(60, 90),
                    'heart_rate': np.random.randint(60, 100),
                    'temperature': np.random.normal(37, 0.3)
                })
        
        pd.DataFrame(vitals).to_sql('vital_signs', conn, if_exists='replace', index=False)
        conn.close()
    
    def _clean_patient_data(self, df):
        """Clean and validate patient information"""
        df = df.copy()
        
        # Convert dates to datetime
        df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])
        
        # Standardize sex values
        df['sex'] = df['sex'].map({'M': 'Male', 'F': 'Female'})
        
        # Handle missing values
        df['age'] = df['age'].fillna(df['age'].median())
        
        return df
    
    def _clean_lab_results(self, df):
        """Clean and standardize lab results"""
        df = df.copy()
        
        # Convert dates
        df['test_date'] = pd.to_datetime(df['test_date'])
        
        # Remove outliers (simple z-score method)
        df['z_score'] = (df['value'] - df.groupby('test_name')['value'].transform('mean')) / \
                       df.groupby('test_name')['value'].transform('std')
        df = df[abs(df['z_score']) < 3].drop('z_score', axis=1)
        
        return df
    
    def _clean_vital_signs(self, df):
        """Clean vital signs data"""
        df = df.copy()
        
        # Convert dates
        df['measurement_date'] = pd.to_datetime(df['measurement_date'])
        
        # Remove physiologically impossible values
        df = df[
            (df['systolic_bp'] > df['diastolic_bp']) & 
            (df['systolic_bp'] < 200) & 
            (df['diastolic_bp'] > 40) &
            (df['heart_rate'].between(40, 200)) &
            (df['temperature'].between(35, 40))
        ]
        
        return df
    
    def _create_derived_features(self, patients, labs, vitals):
        """Create derived features and combine datasets"""
        
        # Calculate average vital signs per patient
        vital_stats = vitals.groupby('patient_id').agg({
            'systolic_bp': ['mean', 'std'],
            'diastolic_bp': ['mean', 'std'],
            'heart_rate': ['mean', 'std']
        }).round(2)
        vital_stats.columns = ['_'.join(col).strip() for col in vital_stats.columns]
        vital_stats = vital_stats.reset_index()
        
        # Calculate lab result statistics
        lab_stats = labs.groupby(['patient_id', 'test_name'])['value'].agg(['mean', 'std']).round(2)
        lab_stats = lab_stats.reset_index().pivot(
            index='patient_id',
            columns='test_name',
            values=['mean', 'std']
        )
        lab_stats.columns = ['_'.join(col).strip() for col in lab_stats.columns]
        lab_stats = lab_stats.reset_index()
        
        # Combine all features
        enriched_data = {
            'patient_info': patients,
            'vital_stats': vital_stats,
            'lab_stats': lab_stats
        }
        
        return enriched_data
    
    def _generate_summary_report(self, enriched_data):
        """Generate summary report of the processed data"""
        report_path = self.output_path / 'etl_summary_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("ETL Pipeline Summary Report\n")
            f.write("=========================\n\n")
            
            # Write processing log
            f.write("Processing Log:\n")
            for log_entry in self.log:
                f.write(f"- {log_entry}\n")
            
            # Write data summaries
            f.write("\nProcessed Data Summary:\n")
            for name, data in enriched_data.items():
                f.write(f"\n{name.replace('_', ' ').title()}:\n")
                f.write(f"- Records: {len(data)}\n")
                f.write(f"- Columns: {', '.join(data.columns)}\n")
            
            f.write("\nETL Pipeline completed successfully\n")

def run_etl_pipeline():
    """Run the complete ETL pipeline"""
    print("Starting ETL Pipeline...")
    
    # Initialize ETL pipeline
    etl = ClinicalDataETL()
    
    # Extract data
    lab_results, patient_info, vitals = etl.extract_data()
    
    # Transform data
    enriched_data = etl.transform_data(lab_results, patient_info, vitals)
    
    # Load data
    etl.load_data(enriched_data)
    
    print("\nETL Pipeline completed successfully!")
    print("Check the 'data' directory for outputs and reports.")

if __name__ == "__main__":
    run_etl_pipeline()