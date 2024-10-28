# data_validation.py - Validating and verifying clinical data
# This script demonstrates various validation techniques to ensure data quality
# and consistency in clinical datasets, including range checks, relationship
# validation, and temporal consistency checks.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Create visualization directory
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Loading and preparing sample data")

def load_sample_data():
    """
    Load or create sample clinical data for validation
    Returns both raw and processed datasets to validate transformations
    """
    # Create sample clinical data with some intentional issues
    np.random.seed(42)
    n_patients = 200
    n_visits = 4
    
    data = []
    for patient_id in range(n_patients):
        age = np.random.randint(18, 90)
        weight_baseline = np.random.normal(70, 15)
        height = np.random.normal(170, 10)
        
        for visit in range(n_visits):
            # Add some realistic variation and occasional errors
            record = {
                'patient_id': f'P{patient_id:03d}',
                'visit_number': visit + 1,
                'visit_date': pd.Timestamp('2023-01-01') + pd.Timedelta(days=30*visit) + 
                            pd.Timedelta(days=np.random.randint(-5, 5)),
                'age': age + (1 if visit > 2 else 0),  # Age increases after 6 months
                'height': height + np.random.normal(0, 0.5),  # Small measurement variations
                'weight': weight_baseline + np.random.normal(0, 2),  # Normal weight fluctuation
                'systolic_bp': np.random.normal(120, 10),
                'diastolic_bp': np.random.normal(80, 8),
                'heart_rate': np.random.normal(75, 10),
                'temperature': np.random.normal(37, 0.3),
                'glucose': np.random.normal(100, 15),
            }
            
            # Add some intentional errors for validation testing (1% of records)
            if np.random.random() < 0.01:
                error_type = np.random.choice(['range', 'relationship', 'temporal'])
                if error_type == 'range':
                    record['temperature'] = np.random.choice([35, 41])  # Implausible temperatures
                elif error_type == 'relationship':
                    record['diastolic_bp'] = record['systolic_bp'] + 10  # Impossible BP relationship
                elif error_type == 'temporal':
                    record['visit_date'] = record['visit_date'] - pd.Timedelta(days=180)  # Time inconsistency
            
            data.append(record)
    
    return pd.DataFrame(data)

# Load the data
df = load_sample_data()
print("\nInitial data shape:", df.shape)
print("\nSample of loaded data:")
print(df.head())

print("\n2. Define validation rules")

class ClinicalDataValidator:
    """Class to handle clinical data validation rules and checks"""
    
    def __init__(self):
        # Define valid ranges for clinical measurements
        self.valid_ranges = {
            'age': (18, 100),
            'height': (140, 220),  # cm
            'weight': (35, 250),   # kg
            'systolic_bp': (70, 200),
            'diastolic_bp': (40, 120),
            'heart_rate': (40, 150),
            'temperature': (35.5, 40.0),
            'glucose': (30, 500)
        }
    
    def check_ranges(self, df):
        """Check if values fall within expected ranges"""
        range_violations = pd.DataFrame(index=df.index)
        
        for column, (min_val, max_val) in self.valid_ranges.items():
            if column in df.columns:
                violations = ~df[column].between(min_val, max_val)
                range_violations[f'{column}_range_violation'] = violations
        
        return range_violations
    
    def check_relationships(self, df):
        """Check if relationships between variables are valid"""
        relationship_violations = pd.DataFrame(index=df.index)
        
        # Check blood pressure relationship
        bp_violation = df['diastolic_bp'] >= df['systolic_bp']
        relationship_violations['bp_relationship_violation'] = bp_violation
        
        # Check BMI range
        bmi = df['weight'] / ((df['height']/100) ** 2)
        bmi_violation = ~bmi.between(10, 60)
        relationship_violations['bmi_range_violation'] = bmi_violation
        
        return relationship_violations
    
    def check_temporal_consistency(self, df):
        """Check temporal consistency of measurements"""
        temporal_violations = pd.DataFrame(index=df.index)
        
        # Check visit dates are properly ordered
        date_violations = df.groupby('patient_id').apply(
            lambda x: x['visit_date'].diff().dt.days < 0
        ).reset_index(level=0, drop=True)
        
        temporal_violations['visit_date_violation'] = date_violations
        
        # Check age consistency
        age_violations = df.groupby('patient_id').apply(
            lambda x: x['age'].diff().abs() > 1
        ).reset_index(level=0, drop=True)
        
        temporal_violations['age_consistency_violation'] = age_violations
        
        return temporal_violations
    
    def validate_data(self, df):
        """Run all validation checks"""
        range_violations = self.check_ranges(df)
        relationship_violations = self.check_relationships(df)
        temporal_violations = self.check_temporal_consistency(df)
        
        # Combine all violations
        all_violations = pd.concat([
            range_violations,
            relationship_violations,
            temporal_violations
        ], axis=1)
        
        return all_violations

print("\n3. Perform validation checks")

# Initialize validator and run checks
validator = ClinicalDataValidator()
violations = validator.validate_data(df)

# Summarize violations
violation_summary = violations.sum().to_frame('count').reset_index()
violation_summary.columns = ['violation_type', 'count']
violation_summary = violation_summary[violation_summary['count'] > 0]

print("\nValidation summary:")
print(violation_summary)

print("\n4. Visualize validation results")

# Create violation patterns visualization
plt.figure(figsize=(12, 6))
sns.heatmap(violations.T, cmap='YlOrRd', cbar_kws={'label': 'Violation Present'})
plt.title('Data Validation Violations Pattern')
plt.xlabel('Record Index')
plt.ylabel('Validation Check')
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'violation_patterns.png'))
plt.close()

# Create violation counts visualization
plt.figure(figsize=(10, 6))
violation_summary.plot(kind='bar', x='violation_type', y='count')
plt.title('Validation Violations by Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'violation_counts.png'))
plt.close()

print("\n5. Generate detailed violation report")

def generate_violation_report(df, violations):
    """Generate detailed report of violations"""
    report = []
    
    # For each record with violations
    for idx in violations.index[violations.any(axis=1)]:
        record = df.loc[idx]
        record_violations = violations.loc[idx]
        
        for check in record_violations[record_violations].index:
            report.append({
                'patient_id': record['patient_id'],
                'visit_number': record['visit_number'],
                'violation_type': check,
                'relevant_values': get_relevant_values(record, check)
            })
    
    return pd.DataFrame(report)

def get_relevant_values(record, violation_type):
    """Extract relevant values for the violation type"""
    if 'range' in violation_type:
        variable = violation_type.replace('_range_violation', '')
        # Check if the variable exists in the record
        if variable in record:
            return f"{variable}: {record[variable]}"
        return "N/A"
    elif 'bp_relationship' in violation_type:
        return f"Systolic: {record['systolic_bp']}, Diastolic: {record['diastolic_bp']}"
    elif 'bmi_range' in violation_type:
        height = record['height']
        weight = record['weight']
        bmi = weight / ((height/100) ** 2)
        return f"BMI: {bmi:.1f} (height: {height}, weight: {weight})"
    elif 'visit_date' in violation_type:
        return f"Visit date: {record['visit_date']}"
    elif 'age_consistency' in violation_type:
        return f"Age: {record['age']}"
    return "N/A"

violation_report = generate_violation_report(df, violations)
print("\nDetailed violation report:")
print(violation_report.head())

print("\n6. Data quality metrics")

def calculate_quality_metrics(df, violations):
    """Calculate various data quality metrics"""
    metrics = {
        'total_records': len(df),
        'clean_records': len(df) - len(violations[violations.any(axis=1)]),
        'violation_rate': (len(violations[violations.any(axis=1)]) / len(df)) * 100,
        'completeness': (1 - df.isnull().sum() / len(df)) * 100,
        'unique_patients': df['patient_id'].nunique(),
        'avg_visits_per_patient': df.groupby('patient_id').size().mean()
    }
    
    return pd.Series(metrics)

quality_metrics = calculate_quality_metrics(df, violations)
print("\nData quality metrics:")
print(quality_metrics)

print("\n7. Export validation results")

# Create results directory
results_dir = 'validation_results'
os.makedirs(results_dir, exist_ok=True)

# Save validation results
violations.to_csv(os.path.join(results_dir, 'validation_violations.csv'))
violation_report.to_csv(os.path.join(results_dir, 'violation_report.csv'))
quality_metrics.to_frame().to_csv(os.path.join(results_dir, 'quality_metrics.csv'))

# Create validation summary report
with open(os.path.join(results_dir, 'validation_summary.txt'), 'w') as f:
    f.write("Clinical Data Validation Summary\n")
    f.write("==============================\n\n")
    f.write(f"Total records analyzed: {len(df)}\n")
    f.write(f"Number of patients: {df['patient_id'].nunique()}\n")
    f.write(f"Time period: {df['visit_date'].min()} to {df['visit_date'].max()}\n\n")
    f.write("Quality Metrics:\n")
    f.write(quality_metrics.to_string())
    f.write("\n\nValidation Violations:\n")
    f.write(violation_summary.to_string())

print("\nValidation complete! Check the visualization_assets folder for plots")
print("and validation_results directory for detailed reports.")