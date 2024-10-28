# data_merging.py - Combining multiple biological datasets
# This script demonstrates various techniques for merging and combining different types
# of biological data, such as gene expression, protein levels, and clinical outcomes.
# In real research, we often need to integrate data from multiple sources or experiments.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set up visualization directory in root folder
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample datasets")

# Set random seed for reproducibility
np.random.seed(42)

# Generate gene expression data
# In real scenarios, this might come from RNA-seq or microarray experiments
def create_expression_data(n_patients=100, n_genes=50):
    """
    Create synthetic gene expression data
    Parameters:
        n_patients: number of patients
        n_genes: number of genes measured
    Returns:
        DataFrame with gene expression values
    """
    patient_ids = [f'PT_{i:03d}' for i in range(n_patients)]
    gene_ids = [f'GENE_{i:03d}' for i in range(n_genes)]
    
    # Generate random expression values (log2 scale)
    data = np.random.normal(loc=6, scale=2, size=(n_patients, n_genes))
    
    return pd.DataFrame(data, index=patient_ids, columns=gene_ids)

# Generate protein measurement data
# This could represent mass spectrometry or Western blot data
def create_protein_data(n_patients=100, n_proteins=30):
    """
    Create synthetic protein measurement data
    Parameters:
        n_patients: number of patients
        n_proteins: number of proteins measured
    Returns:
        DataFrame with protein levels
    """
    data = []
    for pt_idx in range(n_patients):
        patient_id = f'PT_{pt_idx:03d}'
        for prot_idx in range(n_proteins):
            protein_id = f'PROT_{prot_idx:03d}'
            # Protein measurements often have some missing values
            if np.random.random() > 0.1:  # 10% missing data
                level = np.random.normal(100, 20)
                data.append({
                    'patient_id': patient_id,
                    'protein_id': protein_id,
                    'protein_level': level,
                    'detection_quality': 'High' if level > 80 else 'Low'
                })
    
    return pd.DataFrame(data)

# Generate clinical data
# This represents patient metadata and clinical outcomes
def create_clinical_data(n_patients=100):
    """
    Create synthetic clinical data
    Returns:
        DataFrame with patient clinical information
    """
    patient_ids = [f'PT_{i:03d}' for i in range(n_patients)]
    
    return pd.DataFrame({
        'patient_id': patient_ids,
        'age': np.random.normal(60, 10, n_patients).astype(int),
        'sex': np.random.choice(['M', 'F'], n_patients),
        'disease_stage': np.random.choice(['I', 'II', 'III', 'IV'], n_patients),
        'treatment_response': np.random.choice(['Complete', 'Partial', 'None'], n_patients),
        'survival_months': np.random.exponential(24, n_patients).astype(int)
    })

# Create our sample datasets
print("\nGenerating sample datasets...")
expression_df = create_expression_data()
protein_df = create_protein_data()
clinical_df = create_clinical_data()

print("Dataset shapes:")
print(f"Expression data: {expression_df.shape}")
print(f"Protein data: {protein_df.shape}")
print(f"Clinical data: {clinical_df.shape}")

print("\n2. Basic merging operations")

# Reshape expression data for merging
# Convert from wide to long format
expr_long = expression_df.reset_index().melt(
    id_vars=['index'],
    var_name='gene_id',
    value_name='expression_level'
).rename(columns={'index': 'patient_id'})

print("\nMerging clinical data with expression data")
# Merge clinical data with gene expression data
# This links patient outcomes with their gene expression profiles
clinical_expr = clinical_df.merge(
    expr_long,
    on='patient_id',
    how='inner'  # Only keep patients with both clinical and expression data
)
print("Shape after merge:", clinical_expr.shape)

print("\n3. Advanced merging operations")

# Create a more complex merge with protein data
# First, reshape protein data for specific genes of interest
protein_pivot = protein_df.pivot(
    index='patient_id',
    columns='protein_id',
    values='protein_level'
)

# Perform multi-level merge
def create_integrated_dataset():
    """
    Create an integrated dataset combining all data sources
    Uses multiple merge operations and handles missing data
    """
    # Start with clinical data
    integrated = clinical_df.copy()
    
    # Add mean expression levels per patient
    patient_expr_means = expression_df.mean(axis=1).reset_index()
    patient_expr_means.columns = ['patient_id', 'mean_expression']
    integrated = integrated.merge(
        patient_expr_means,
        on='patient_id',
        how='left'
    )
    
    # Add protein data
    integrated = integrated.merge(
        protein_pivot,
        on='patient_id',
        how='left'
    )
    
    return integrated

integrated_df = create_integrated_dataset()
print("\nIntegrated dataset shape:", integrated_df.shape)

print("\n4. Handling missing data")

# Analyze missing data patterns
def analyze_missing_data(df):
    """
    Analyze patterns of missing data across the integrated dataset
    """
    missing_summary = pd.DataFrame({
        'missing_count': df.isnull().sum(),
        'missing_percent': (df.isnull().sum() / len(df) * 100).round(2)
    }).sort_values('missing_percent', ascending=False)
    
    return missing_summary

missing_analysis = analyze_missing_data(integrated_df)
print("\nMissing data analysis:")
print(missing_analysis[missing_analysis['missing_count'] > 0])

# Visualize missing data patterns
plt.figure(figsize=(10, 6))
plt.bar(
    range(len(missing_analysis)),
    missing_analysis['missing_percent'],
    alpha=0.5
)
plt.title('Missing Data by Column')
plt.xlabel('Column Index')
plt.ylabel('Percent Missing')
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'missing_data_patterns.png'))
plt.close()

print("\n5. Creating analysis-ready datasets")

def prepare_analysis_dataset(integrated_df, missing_threshold=50):
    """
    Prepare final dataset for analysis by handling missing data
    Parameters:
        integrated_df: The merged dataset
        missing_threshold: Maximum percentage of missing data allowed per column
    """
    # Remove columns with too many missing values
    missing_percents = (integrated_df.isnull().sum() / len(integrated_df) * 100)
    columns_to_keep = missing_percents[missing_percents < missing_threshold].index
    
    # Create analysis dataset
    analysis_df = integrated_df[columns_to_keep].copy()
    
    # Fill missing values appropriately
    # Numeric columns: fill with median
    numeric_columns = analysis_df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        analysis_df[col].fillna(analysis_df[col].median(), inplace=True)
    
    # Categorical columns: fill with mode
    categorical_columns = analysis_df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        analysis_df[col].fillna(analysis_df[col].mode()[0], inplace=True)
    
    return analysis_df

# Create final analysis dataset
analysis_ready_df = prepare_analysis_dataset(integrated_df)
print("\nAnalysis-ready dataset shape:", analysis_ready_df.shape)

print("\n6. Creating summary visualizations")

# Create visualization of data relationships
def plot_data_relationships(df):
    """
    Create visualization showing relationships between different data types
    """
    # Select numeric columns for correlation analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()
    
    plt.figure(figsize=(12, 8))
    plt.imshow(correlations, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Correlation')
    plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45, ha='right')
    plt.yticks(range(len(numeric_cols)), numeric_cols)
    plt.title('Correlations Across Integrated Dataset')
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_path, 'data_correlations.png'))
    plt.close()

plot_data_relationships(analysis_ready_df)

print("\n7. Exporting results")

# Create results directory
results_dir = 'merged_results'
os.makedirs(results_dir, exist_ok=True)

# Save various versions of the data
analysis_ready_df.to_csv(os.path.join(results_dir, 'analysis_ready_data.csv'))
missing_analysis.to_csv(os.path.join(results_dir, 'missing_data_analysis.csv'))

# Create a data summary report
with open(os.path.join(results_dir, 'data_summary.txt'), 'w') as f:
    f.write("Integrated Dataset Summary\n")
    f.write("========================\n\n")
    f.write(f"Number of patients: {len(analysis_ready_df)}\n")
    f.write(f"Number of features: {len(analysis_ready_df.columns)}\n")
    f.write(f"Clinical variables: {len(clinical_df.columns)}\n")
    f.write(f"Number of genes: {len(expression_df.columns)}\n")
    f.write(f"Number of proteins: {len(protein_pivot.columns)}\n")

print("\nData merging complete! Check the visualization_assets folder for plots")
print("and merged_results directory for the final datasets and summaries.")