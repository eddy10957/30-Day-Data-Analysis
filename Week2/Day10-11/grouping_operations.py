# grouping_operations.py - Advanced grouping and aggregation techniques
# This script demonstrates advanced Pandas grouping operations using biological experiment data,
# showing how to analyze and summarize complex experimental results across different conditions.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set up the visualization directory in the root folder
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample biological experiment data")

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic experimental data that mimics a large-scale biological study
# This could represent, for example, a flow cytometry experiment measuring
# protein levels and gene expression across different cell types and treatments
n_experiments = 1000  # Number of individual experiments/measurements

# Create a comprehensive dataset with multiple variables
data = {
    'experiment_id': [f'EXP_{i:04d}' for i in range(n_experiments)],
    # Protein levels typically follow a normal distribution in log-space
    'protein_level': np.random.normal(100, 15, n_experiments),
    # Gene expression values also typically follow a normal distribution
    'gene_expression': np.random.normal(50, 10, n_experiments),
    # Different cell types being studied
    'cell_type': np.random.choice(['T-cell', 'B-cell', 'NK-cell'], n_experiments),
    # Different treatment conditions
    'treatment': np.random.choice(['Control', 'Drug A', 'Drug B', 'Drug C'], n_experiments),
    # Time points for temporal analysis
    'time_point': np.random.choice(['0h', '6h', '12h', '24h'], n_experiments),
    # Experimental batches to account for technical variation
    'batch': np.random.choice(['Batch1', 'Batch2', 'Batch3'], n_experiments),
    # Temperature during experiment (should be close to 37°C)
    'temperature': np.random.normal(37, 0.5, n_experiments),
    # Binary success indicator for quality control
    'success': np.random.choice([True, False], n_experiments, p=[0.9, 0.1])
}

# Create DataFrame from our synthetic data
df = pd.DataFrame(data)

print("\n2. Basic grouping operations")

# Perform simple groupby operations with multiple aggregation functions
# This gives us an overview of how measurements vary across cell types
basic_stats = df.groupby('cell_type').agg({
    'protein_level': ['count', 'mean', 'std'],  # Basic statistics for protein levels
    'gene_expression': ['mean', 'std']          # Basic statistics for gene expression
})
print("\nBasic statistics by cell type:")
print(basic_stats)

print("\n3. Advanced grouping operations")

# Define custom aggregation function for more specific analysis
def quartile_range(x):
    """Calculate the interquartile range (IQR)
    IQR is a robust measure of variability, less sensitive to outliers than std"""
    return x.quantile(0.75) - x.quantile(0.25)

# Perform complex grouping with multiple keys and custom aggregations
advanced_stats = df.groupby(['cell_type', 'treatment']).agg({
    'protein_level': [
        'count',                                # Number of measurements
        'mean',                                 # Average protein level
        'std',                                  # Standard deviation
        quartile_range,                         # Custom IQR function
        lambda x: x.quantile(0.95)              # 95th percentile
    ],
    'gene_expression': [
        'mean',
        'std',
        quartile_range
    ]
}).round(2)

print("\nAdvanced statistics by cell type and treatment:")
print(advanced_stats)

print("\n4. Transform and filter operations")

# Calculate z-scores within each cell type group
# This normalizes measurements relative to other cells of the same type
df['protein_z_score'] = df.groupby('cell_type')['protein_level'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Filter groups based on size and variability criteria
# This helps focus on groups with sufficient data and interesting variation
significant_groups = df.groupby(['cell_type', 'treatment']).filter(
    lambda x: (len(x) >= 20) &                  # At least 20 measurements
             (x['protein_level'].std() > 10)     # Substantial variation
)

print("\nNumber of significant groups:", len(significant_groups['cell_type'].unique()))

print("\n5. Window operations")

# Sort values for meaningful window calculations
df_sorted = df.sort_values('protein_level')

# Calculate rolling statistics within groups
# This helps identify trends and patterns in sorted data
rolling_stats = df_sorted.groupby('cell_type')['protein_level'].rolling(
    window=20,      # Calculate over windows of 20 measurements
    min_periods=5   # Require at least 5 measurements for calculation
).agg(['mean', 'std'])

print("\nRolling statistics example:")
print(rolling_stats.head())

print("\n6. Complex transformations")

# Calculate experiment success rates by group
# This helps identify conditions that might be problematic
success_rate = df.groupby(['cell_type', 'treatment'])['success'].agg([
    'count',                                    # Total number of experiments
    ('success_rate', 'mean')                    # Proportion of successful experiments
]).round(3) * 100  # Convert to percentage

print("\nSuccess rate by group:")
print(success_rate)

# Visualize success rates across different conditions
plt.figure(figsize=(12, 6))
success_pivot = success_rate.reset_index().pivot(
    index='cell_type',
    columns='treatment',
    values='success_rate'
)
success_pivot.plot(kind='bar')
plt.title('Experiment Success Rate by Cell Type and Treatment')
plt.xlabel('Cell Type')
plt.ylabel('Success Rate (%)')
plt.legend(title='Treatment')
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'success_rates.png'))
plt.close()

print("\n7. Advanced analysis")

# Create cross-tabulation of categorical variables
# This shows how experiments are distributed across conditions
cross_tab = pd.crosstab(
    [df['cell_type'], df['treatment']],
    df['time_point'],
    margins=True  # Add row and column totals
)
print("\nCross-tabulation of experiments:")
print(cross_tab)

# Perform correlation analysis within groups
def group_correlations(group):
    """Calculate correlations between different measurements within each group"""
    return pd.Series({
        'protein_gene_corr': group['protein_level'].corr(group['gene_expression']),
        'protein_temp_corr': group['protein_level'].corr(group['temperature'])
    })

# Calculate correlations for each combination of cell type and treatment
correlations = df.groupby(['cell_type', 'treatment']).apply(group_correlations)
print("\nCorrelation analysis by group:")
print(correlations)

# Export results for further analysis
print("\n8. Exporting results")

# Create results directory
results_dir = 'grouping_results'
os.makedirs(results_dir, exist_ok=True)

# Save various analysis results
advanced_stats.to_csv(os.path.join(results_dir, 'advanced_stats.csv'))
success_rate.to_csv(os.path.join(results_dir, 'success_rates.csv'))
correlations.to_csv(os.path.join(results_dir, 'correlations.csv'))

print("\nGrouping analysis complete! Check the visualization_assets folder for plots")
print("and grouping_results directory for detailed statistics.")