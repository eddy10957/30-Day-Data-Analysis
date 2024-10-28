# advanced_transformations.py - Complex data manipulations with gene expression data

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create sample gene expression data
print("1. Creating sample gene expression dataset")

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic gene expression data
# In real experiments, gene expression is typically measured for multiple genes
# across different samples/conditions using techniques like RNA-seq or microarrays
n_genes = 100  # Number of genes to simulate
n_samples = 20  # Number of experimental samples
gene_names = [f'GENE_{i:03d}' for i in range(n_genes)]  # Generate gene identifiers
sample_names = [f'SAMPLE_{i:02d}' for i in range(n_samples)]  # Generate sample identifiers

# Generate random expression values
# We use normal distribution with mean=5 and std=2 to simulate log2 expression values
# Real gene expression data often follows a log-normal distribution
expression_data = np.random.normal(loc=5, scale=2, size=(n_genes, n_samples))

# Create the main dataframe
# Rows represent genes, columns represent samples (standard format for expression data)
df = pd.DataFrame(expression_data, index=gene_names, columns=sample_names)

# Create sample metadata
# In real experiments, each sample has associated metadata like treatment conditions,
# time points, and batch information which is crucial for analysis
sample_metadata = pd.DataFrame({
    'sample_id': sample_names,
    # Samples are divided into control and treatment groups
    'condition': np.random.choice(['Control', 'Treatment A', 'Treatment B'], n_samples),
    # Time points represent when samples were collected after treatment
    'time_point': np.random.choice(['0h', '12h', '24h', '48h'], n_samples),
    # Batch information is important for controlling technical variation
    'batch': np.random.choice(['Batch1', 'Batch2'], n_samples)
})

print("\n2. Exploring data transformations")

# Melt the expression matrix
# Melting transforms the wide format (genes x samples) into long format
# This is often necessary for certain types of analyses and visualizations
print("\nMelting expression matrix")
melted_df = df.reset_index().melt(
    id_vars=['index'],  # Keep gene IDs as identifier
    var_name='sample_id',  # Sample IDs become a column
    value_name='expression'  # Expression values become a column
)
melted_df = melted_df.rename(columns={'index': 'gene_id'})
print(melted_df.head())

# Merge with metadata
# Combining expression data with sample metadata is crucial for analysis
# This links each expression measurement with its experimental conditions
print("\nMerging with metadata")
merged_df = melted_df.merge(sample_metadata, on='sample_id')
print(merged_df.head())

print("\n3. Performing complex transformations")

# Z-score normalization
# This transforms expression values to standard deviations from the mean
# Useful for comparing expression patterns across genes with different baseline levels
def calculate_zscore(group):
    """
    Calculate z-scores for a group of values
    Z-score = (value - mean) / standard deviation
    This normalizes the data to have mean=0 and std=1
    """
    return (group - group.mean()) / group.std()

print("\nCalculating z-scores")
zscore_df = df.apply(calculate_zscore)
print(zscore_df.head())

# Create pivot table for condition and time analysis
# This restructures the data to show average expression for each combination
# of experimental conditions, making it easier to spot patterns
print("\nCreating pivot table")
pivot_df = pd.pivot_table(
    merged_df,
    values='expression',
    index='gene_id',
    columns=['condition', 'time_point'],
    aggfunc='mean'  # Calculate mean expression for each condition/time combination
)
print(pivot_df.head())

print("\n4. Calculating fold changes")

def calculate_fold_changes(df, control_condition='Control'):
    """
    Calculate log2 fold changes between treatment and control conditions
    Fold change is a common measure of differential expression:
    - log2(FC) > 0 indicates upregulation
    - log2(FC) < 0 indicates downregulation
    """
    # Get control samples
    control_samples = sample_metadata[
        sample_metadata['condition'] == control_condition
    ]['sample_id']
    
    # Calculate mean expression for control condition
    control_mean = df[control_samples].mean(axis=1)
    
    # Calculate fold changes for each treatment condition
    fold_changes = pd.DataFrame(index=df.index)
    for condition in sample_metadata['condition'].unique():
        if condition != control_condition:
            # Get samples for this condition
            condition_samples = sample_metadata[
                sample_metadata['condition'] == condition
            ]['sample_id']
            # Calculate mean expression for treatment
            condition_mean = df[condition_samples].mean(axis=1)
            # Calculate log2 fold change
            fold_changes[f'FC_{condition}'] = np.log2(condition_mean / control_mean)
    
    return fold_changes

fold_changes = calculate_fold_changes(df)
print(fold_changes.head())

print("\n5. Performing advanced filtering")

def find_significant_genes(fold_changes, threshold=1.5):
    """
    Find genes with significant expression changes
    threshold: minimum absolute log2 fold change to be considered significant
    Returns dictionary with lists of significant genes for each condition
    """
    significant_genes = {}
    for column in fold_changes.columns:
        # Get genes with absolute fold change above threshold
        sig_genes = fold_changes[
            abs(fold_changes[column]) > threshold
        ].index.tolist()
        significant_genes[column] = sig_genes
    return significant_genes

significant_genes = find_significant_genes(fold_changes)
print("\nNumber of significant genes per condition:")
for condition, genes in significant_genes.items():
    print(f"{condition}: {len(genes)}")

print("\n6. Demonstrating batch correction")

def simple_batch_correction(df, batch_info):
    """
    Perform simple mean-centering batch correction
    This removes technical variation between batches while preserving
    biological variation of interest
    
    """
    # Calculate mean expression for each batch
    batch_means = {}
    corrected_df = df.copy()
    
    # Calculate mean expression level for each batch
    for batch in batch_info['batch'].unique():
        batch_samples = batch_info[batch_info['batch'] == batch]['sample_id']
        batch_means[batch] = df[batch_samples].mean().mean()
    
    # Center each batch by adjusting to global mean
    global_mean = np.mean(list(batch_means.values()))
    for batch in batch_means:
        batch_samples = batch_info[batch_info['batch'] == batch]['sample_id']
        correction_factor = global_mean - batch_means[batch]
        corrected_df[batch_samples] += correction_factor
    
    return corrected_df

corrected_df = simple_batch_correction(df, sample_metadata)
print("\nBatch correction complete")

# Export results
print("\n7. Exporting results")

# Create results directory
results_dir = 'analysis_results'
os.makedirs(results_dir, exist_ok=True)

# Save the processed data for further analysis
fold_changes.to_csv(os.path.join(results_dir, 'fold_changes.csv'))
pivot_df.to_csv(os.path.join(results_dir, 'expression_by_condition.csv'))

# Save list of significant genes
with open(os.path.join(results_dir, 'significant_genes.txt'), 'w') as f:
    for condition, genes in significant_genes.items():
        f.write(f"\n{condition}:\n")
        f.write('\n'.join(genes))
        f.write('\n')

print("\nAnalysis complete! Results saved in 'analysis_results' directory.")

# Print summary statistics
print("\n8. Summary statistics")
print("\nShape of original data:", df.shape)
print("Shape of pivot table:", pivot_df.shape)
print("Number of conditions:", len(sample_metadata['condition'].unique()))
print("Number of time points:", len(sample_metadata['time_point'].unique()))
print("Total significant genes:", sum(len(genes) for genes in significant_genes.values()))