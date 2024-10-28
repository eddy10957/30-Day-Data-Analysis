# feature_engineering.py - Creating new features from clinical data
# This script demonstrates various feature engineering techniques commonly used
# in clinical data analysis, showing how to derive meaningful features from raw data.

import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import matplotlib.pyplot as plt
import os

# Create visualization directory
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Loading and preparing sample clinical data")

def create_clinical_dataset(n_patients=500):
    """
    Create a synthetic clinical dataset with multiple measurements over time
    This simulates a longitudinal study with various patient measurements
    """
    np.random.seed(42)
    
    # Generate base patient data
    patients = []
    start_date = pd.Timestamp('2023-01-01')
    
    for patient_id in range(n_patients):
        # Generate 6 visits per patient over 6 months
        for visit in range(6):
            visit_date = start_date + pd.Timedelta(days=30*visit) + pd.Timedelta(days=np.random.randint(-5, 5))
            
            # Base measurements
            base_bp = np.random.normal(120, 10)
            base_glucose = np.random.normal(100, 15)
            
            # Add some trends over time
            bp_trend = visit * np.random.normal(1, 0.5)
            glucose_trend = visit * np.random.normal(2, 1)
            
            patients.append({
                'patient_id': f'P{patient_id:03d}',
                'visit_number': visit + 1,
                'visit_date': visit_date,
                'age': np.random.randint(30, 80),
                'sex': np.random.choice(['M', 'F']),
                'weight': np.random.normal(70, 15),
                'height': np.random.normal(170, 10),
                'systolic_bp': base_bp + bp_trend,
                'diastolic_bp': (base_bp + bp_trend) * 0.6,
                'heart_rate': np.random.normal(75, 8),
                'glucose': base_glucose + glucose_trend,
                'cholesterol': np.random.normal(200, 30),
                'medication_count': np.random.randint(0, 5)
            })
    
    return pd.DataFrame(patients)

# Create initial dataset
df = create_clinical_dataset()
print("\nInitial dataset shape:", df.shape)
print("\nSample of initial data:")
print(df.head())

print("\n2. Basic feature engineering")

def create_basic_features(df):
    """Create basic derived features from raw measurements"""
    df = df.copy()
    
    # Calculate BMI
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # Calculate pulse pressure (difference between systolic and diastolic)
    df['pulse_pressure'] = df['systolic_bp'] - df['diastolic_bp']
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], 
                            bins=[0, 40, 50, 60, 70, 100],
                            labels=['<40', '40-50', '50-60', '60-70', '>70'])
    
    # Calculate mean arterial pressure
    df['mean_arterial_pressure'] = df['diastolic_bp'] + (df['pulse_pressure'] / 3)
    
    return df

df = create_basic_features(df)
print("\nBasic features added:")
print(df[['bmi', 'pulse_pressure', 'age_group', 'mean_arterial_pressure']].head())

print("\n3. Time-based feature engineering")

def create_temporal_features(df):
    """Create features based on temporal patterns and changes"""
    df = df.copy()
    
    # Add time-based features
    df['visit_date'] = pd.to_datetime(df['visit_date'])
    df['month'] = df['visit_date'].dt.month
    df['day_of_week'] = df['visit_date'].dt.dayofweek
    
    # Calculate days since first visit for each patient
    df['days_since_first_visit'] = df.groupby('patient_id')['visit_date'].transform(
        lambda x: (x - x.min()).dt.days
    )
    
    # Calculate changes from previous visit
    for col in ['weight', 'systolic_bp', 'glucose']:
        df[f'{col}_change'] = df.groupby('patient_id')[col].diff()
        
        # Calculate rate of change (per 30 days)
        df[f'{col}_rate_change'] = (
            df[f'{col}_change'] / 
            df.groupby('patient_id')['days_since_first_visit'].diff()
        ) * 30
    
    return df

df = create_temporal_features(df)
print("\nTemporal features added:")
print(df[['days_since_first_visit', 'weight_change', 'weight_rate_change']].head())

print("\n4. Statistical feature engineering")

def create_statistical_features(df):
    """Create features based on statistical calculations"""
    df = df.copy()
    
    # Calculate rolling means and standard deviations
    for col in ['systolic_bp', 'glucose', 'heart_rate']:
        # Calculate rolling statistics for each patient
        df[f'{col}_rolling_mean'] = df.groupby('patient_id')[col].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        df[f'{col}_rolling_std'] = df.groupby('patient_id')[col].transform(
            lambda x: x.rolling(window=3, min_periods=1).std()
        )
        
        # Calculate z-scores within patient
        df[f'{col}_zscore'] = df.groupby('patient_id')[col].transform(
            lambda x: stats.zscore(x, nan_policy='omit')
        )
    
    return df

df = create_statistical_features(df)
print("\nStatistical features added:")
print(df[['systolic_bp_rolling_mean', 'systolic_bp_rolling_std', 'systolic_bp_zscore']].head())

print("\n5. Interaction features")

def create_interaction_features(df):
    """Create features that capture interactions between different measurements"""
    df = df.copy()
    
    # Create interaction terms
    df['bp_glucose_interaction'] = df['systolic_bp'] * df['glucose']
    df['bmi_age_interaction'] = df['bmi'] * df['age']
    
    # Create composite risk scores
    df['cardiovascular_risk_score'] = (
        df['systolic_bp_zscore'] + 
        df['cholesterol_zscore'] + 
        df['bmi_zscore']
    ) / 3
    
    return df

# Calculate z-scores for risk score components first
for col in ['systolic_bp', 'cholesterol', 'bmi']:
    df[f'{col}_zscore'] = stats.zscore(df[col])

df = create_interaction_features(df)
print("\nInteraction features added:")
print(df[['bp_glucose_interaction', 'cardiovascular_risk_score']].head())

print("\n6. Creating visualizations of engineered features")

# Visualize changes over time
plt.figure(figsize=(12, 6))
for patient in df['patient_id'].unique()[:5]:  # Plot first 5 patients
    patient_data = df[df['patient_id'] == patient]
    plt.plot(patient_data['days_since_first_visit'], 
             patient_data['systolic_bp'],
             'o-', label=f'Patient {patient}')
plt.xlabel('Days Since First Visit')
plt.ylabel('Systolic BP')
plt.title('Blood Pressure Trends by Patient')
plt.legend()
plt.savefig(os.path.join(visualization_path, 'bp_trends.png'))
plt.close()

# Visualize risk score distribution
plt.figure(figsize=(10, 6))
plt.hist(df['cardiovascular_risk_score'], bins=30)
plt.xlabel('Cardiovascular Risk Score')
plt.ylabel('Frequency')
plt.title('Distribution of Cardiovascular Risk Scores')
plt.savefig(os.path.join(visualization_path, 'risk_score_distribution.png'))
plt.close()

print("\n7. Feature importance analysis")

def analyze_feature_importance(df, target='glucose'):
    """Analyze correlation of features with a target variable"""
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Calculate correlations
    correlations = df[numeric_cols].corr()[target].sort_values(ascending=False)
    
    # Create correlation plot
    plt.figure(figsize=(12, 6))
    correlations[1:11].plot(kind='bar')  # Plot top 10 correlations (excluding self-correlation)
    plt.title(f'Top 10 Feature Correlations with {target}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_path, 'feature_correlations.png'))
    plt.close()
    
    return correlations

correlations = analyze_feature_importance(df, target='glucose')
print("\nTop feature correlations with glucose:")
print(correlations.head(10))

# Export engineered features
print("\n8. Exporting engineered features")

# Create results directory
results_dir = 'engineered_features'
os.makedirs(results_dir, exist_ok=True)

# Save the final dataset
df.to_csv(os.path.join(results_dir, 'clinical_data_with_features.csv'), index=False)

# Save feature definitions and descriptions
feature_definitions = pd.DataFrame({
    'feature': [
        'bmi', 'pulse_pressure', 'mean_arterial_pressure',
        'days_since_first_visit', 'weight_change', 'cardiovascular_risk_score'
    ],
    'description': [
        'Body Mass Index calculated from height and weight',
        'Difference between systolic and diastolic blood pressure',
        'Average blood pressure during cardiac cycle',
        'Number of days since patient\'s first visit',
        'Change in weight from previous visit',
        'Composite score based on BP, cholesterol, and BMI'
    ]
})
feature_definitions.to_csv(os.path.join(results_dir, 'feature_definitions.csv'), index=False)

print("\nFeature engineering complete! Check the visualization_assets folder for plots")
print("and engineered_features directory for the final dataset and documentation.")