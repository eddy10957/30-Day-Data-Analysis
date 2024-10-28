# outlier_detection.py - Methods for identifying and handling outliers in clinical data
# This script demonstrates various techniques for detecting and handling outliers,
# which is crucial for ensuring data quality in clinical research.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope
import os

# Create visualization directory
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample clinical data with outliers")

def create_sample_data(n_samples=1000):
    """
    Create synthetic clinical data with intentional outliers.
    This represents a typical clinical dataset with various measurements.
    """
    np.random.seed(42)
    
    # Generate normal data
    data = {
        'patient_id': [f'PT{i:04d}' for i in range(n_samples)],
        'age': np.random.normal(60, 10, n_samples),
        'heart_rate': np.random.normal(75, 8, n_samples),
        'blood_pressure': np.random.normal(120, 10, n_samples),
        'temperature': np.random.normal(37, 0.3, n_samples),
        'glucose': np.random.normal(100, 15, n_samples),
        'white_blood_cells': np.random.normal(7.5, 1.5, n_samples)
    }
    
    # Add intentional outliers (about 5% of data)
    outlier_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    
    # Add extreme values for different measurements
    data['heart_rate'][outlier_indices] = np.random.choice(
        [np.random.normal(40, 5), np.random.normal(120, 5)],
        size=len(outlier_indices)
    )
    data['blood_pressure'][outlier_indices] = np.random.choice(
        [np.random.normal(80, 5), np.random.normal(180, 5)],
        size=len(outlier_indices)
    )
    
    df = pd.DataFrame(data)
    return df

# Create dataset
df = create_sample_data()
print("\nSample data shape:", df.shape)
print("\nBasic statistics:")
print(df.describe())

print("\n2. Z-score based outlier detection")

def detect_outliers_zscore(df, columns, threshold=3):
    """
    Detect outliers using the z-score method.
    Z-score > threshold (usually 3) indicates potential outliers.
    """
    outliers = pd.DataFrame()
    for column in columns:
        # Calculate z-scores
        z_scores = np.abs(stats.zscore(df[column]))
        # Identify outliers
        outliers[f'{column}_outlier'] = z_scores > threshold
        # Store z-scores
        outliers[f'{column}_zscore'] = z_scores
    
    return outliers

numeric_columns = ['heart_rate', 'blood_pressure', 'temperature', 'glucose', 'white_blood_cells']
outliers_zscore = detect_outliers_zscore(df, numeric_columns)

# Visualize z-score distributions
plt.figure(figsize=(12, 6))
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(2, 3, i)
    plt.hist(outliers_zscore[f'{column}_zscore'], bins=50)
    plt.title(f'{column} Z-scores')
    plt.axvline(x=3, color='r', linestyle='--', label='Threshold')
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'zscore_distributions.png'))
plt.close()

print("\n3. IQR based outlier detection")

def detect_outliers_iqr(df, columns, k=1.5):
    """
    Detect outliers using the Interquartile Range (IQR) method.
    Values beyond k*IQR below Q1 or above Q3 are considered outliers.
    """
    outliers = pd.DataFrame()
    for column in columns:
        # Calculate Q1, Q3, and IQR
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define bounds
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        
        # Identify outliers
        outliers[f'{column}_outlier'] = (df[column] < lower_bound) | (df[column] > upper_bound)
        
    return outliers

outliers_iqr = detect_outliers_iqr(df, numeric_columns)

print("\n4. Multivariate outlier detection")

def detect_outliers_multivariate(df, columns):
    """
    Detect outliers using multivariate analysis (Elliptic Envelope).
    This method considers relationships between variables.
    """
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[columns])
    
    # Fit elliptic envelope
    detector = EllipticEnvelope(contamination=0.1, random_state=42)
    outliers = detector.fit_predict(scaled_data)
    
    return outliers == -1  # True for outliers

multivariate_outliers = detect_outliers_multivariate(df, numeric_columns)

print("\n5. Visualizing outliers")

def plot_outlier_visualization(df, outliers_zscore, outliers_iqr, multivariate_outliers):
    """Create visualizations to compare different outlier detection methods"""
    
    # Create boxplots for each variable
    plt.figure(figsize=(15, 6))
    df.boxplot(column=numeric_columns)
    plt.xticks(rotation=45)
    plt.title('Distribution of Clinical Measurements with Outliers')
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_path, 'boxplots_with_outliers.png'))
    plt.close()
    
    # Create scatter plot of two main variables with outliers highlighted
    plt.figure(figsize=(12, 4))
    
    # Z-score based outliers
    plt.subplot(131)
    outlier_mask = outliers_zscore['heart_rate_outlier'] | outliers_zscore['blood_pressure_outlier']
    plt.scatter(df.loc[~outlier_mask, 'heart_rate'], 
               df.loc[~outlier_mask, 'blood_pressure'],
               alpha=0.5, label='Normal')
    plt.scatter(df.loc[outlier_mask, 'heart_rate'],
               df.loc[outlier_mask, 'blood_pressure'],
               color='red', alpha=0.7, label='Outliers')
    plt.title('Z-score Outliers')
    plt.xlabel('Heart Rate')
    plt.ylabel('Blood Pressure')
    plt.legend()
    
    # IQR based outliers
    plt.subplot(132)
    outlier_mask = outliers_iqr['heart_rate_outlier'] | outliers_iqr['blood_pressure_outlier']
    plt.scatter(df.loc[~outlier_mask, 'heart_rate'],
               df.loc[~outlier_mask, 'blood_pressure'],
               alpha=0.5, label='Normal')
    plt.scatter(df.loc[outlier_mask, 'heart_rate'],
               df.loc[outlier_mask, 'blood_pressure'],
               color='red', alpha=0.7, label='Outliers')
    plt.title('IQR Outliers')
    plt.xlabel('Heart Rate')
    plt.ylabel('Blood Pressure')
    plt.legend()
    
    # Multivariate outliers
    plt.subplot(133)
    plt.scatter(df.loc[~multivariate_outliers, 'heart_rate'],
               df.loc[~multivariate_outliers, 'blood_pressure'],
               alpha=0.5, label='Normal')
    plt.scatter(df.loc[multivariate_outliers, 'heart_rate'],
               df.loc[multivariate_outliers, 'blood_pressure'],
               color='red', alpha=0.7, label='Outliers')
    plt.title('Multivariate Outliers')
    plt.xlabel('Heart Rate')
    plt.ylabel('Blood Pressure')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_path, 'outlier_comparison.png'))
    plt.close()

plot_outlier_visualization(df, outliers_zscore, outliers_iqr, multivariate_outliers)

print("\n6. Handling outliers")

def handle_outliers(df, outliers_zscore, outliers_iqr, multivariate_outliers):
    """
    Demonstrate different methods for handling outliers:
    1. Removal
    2. Capping
    3. Imputation
    """
    handled_dfs = {}
    
    # 1. Remove outliers (based on z-score)
    outlier_mask = outliers_zscore.filter(like='_outlier').any(axis=1)
    handled_dfs['removed'] = df[~outlier_mask].copy()
    
    # 2. Cap outliers at percentile values
    handled_dfs['capped'] = df.copy()
    for column in numeric_columns:
        lower_bound = df[column].quantile(0.01)
        upper_bound = df[column].quantile(0.99)
        handled_dfs['capped'][column] = handled_dfs['capped'][column].clip(lower_bound, upper_bound)
    
    # 3. Impute outliers with median
    handled_dfs['imputed'] = df.copy()
    for column in numeric_columns:
        mask = outliers_zscore[f'{column}_outlier']
        handled_dfs['imputed'].loc[mask, column] = df[column].median()
    
    return handled_dfs

handled_datasets = handle_outliers(df, outliers_zscore, outliers_iqr, multivariate_outliers)

print("\n7. Comparing results")

def compare_results(original_df, handled_datasets):
    """Compare statistics before and after outlier handling"""
    comparison = pd.DataFrame()
    
    # Calculate statistics for original data
    comparison['Original'] = original_df[numeric_columns].mean()
    
    # Calculate statistics for each handled dataset
    for name, handled_df in handled_datasets.items():
        comparison[name.capitalize()] = handled_df[numeric_columns].mean()
    
    return comparison

comparison_stats = compare_results(df, handled_datasets)
print("\nComparison of means after different outlier handling methods:")
print(comparison_stats)

# Export results
results_dir = 'outlier_results'
os.makedirs(results_dir, exist_ok=True)

# Save outlier information
outliers_zscore.to_csv(os.path.join(results_dir, 'zscore_outliers.csv'))
pd.DataFrame({'multivariate_outliers': multivariate_outliers}).to_csv(
    os.path.join(results_dir, 'multivariate_outliers.csv')
)

# Save handled datasets
for name, handled_df in handled_datasets.items():
    handled_df.to_csv(os.path.join(results_dir, f'{name}_data.csv'), index=False)

# Save comparison statistics
comparison_stats.to_csv(os.path.join(results_dir, 'method_comparison.csv'))

print("\nOutlier analysis complete! Check the visualization_assets folder for plots")
print("and outlier_results directory for detailed statistics.")