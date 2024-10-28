# analysis_queries.py - Combining SQL and Python for clinical data analysis

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')

# Ensure the visualization_assets directory exists
os.makedirs(visualization_path, exist_ok=True)


# Connect to the database
conn = sqlite3.connect('clinical_trials.db')

print("1. Loading and analyzing trial data")

# Get treatment response data
response_query = '''
    SELECT 
        t.treatment_name,
        p.condition,
        tr.treatment_response,
        p.age,
        p.sex
    FROM trial_results tr
    JOIN trials t ON tr.trial_id = t.trial_id
    JOIN patients p ON tr.patient_id = p.patient_id
    WHERE tr.completion_status = 'Completed'
'''
df = pd.read_sql_query(response_query, conn)

# Calculate basic statistics
print("\n2. Basic response statistics by treatment")
treatment_stats = df.groupby('treatment_name')['treatment_response'].agg([
    'count', 'mean', 'std', 'min', 'max'
]).round(3)
print(treatment_stats)

# Analyze response by condition
print("\n3. Response analysis by condition")
condition_analysis = df.groupby(['condition', 'treatment_name'])['treatment_response'].mean().unstack()
print(condition_analysis.round(3))

# Create visualization of treatment responses
print("\n4. Creating response visualization")
plt.figure(figsize=(10, 6))
df.boxplot(column='treatment_response', by='treatment_name')
plt.title('Treatment Response Distribution')
plt.suptitle('')  # This removes the automatic suptitle
plt.ylabel('Response Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'treatment_responses.png'))
plt.close()

# Perform statistical tests
print("\n5. Statistical analysis")
treatments = df['treatment_name'].unique()
print("\nANOVA test for treatment differences:")
treatment_groups = [df[df['treatment_name'] == t]['treatment_response'] for t in treatments]
f_stat, p_value = stats.f_oneway(*treatment_groups)
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# Age correlation analysis
print("\n6. Age correlation analysis")
correlation = df.groupby('treatment_name').apply(
    lambda x: stats.pearsonr(x['age'], x['treatment_response'])
)
print("\nCorrelation between age and treatment response:")
for treatment, (r, p) in correlation.items():
    print(f"{treatment}: r={r:.3f}, p={p:.3f}")

# Create age vs response visualization
plt.figure(figsize=(10, 6))
for treatment in treatments:
    mask = df['treatment_name'] == treatment
    plt.scatter(df[mask]['age'], df[mask]['treatment_response'], 
               label=treatment, alpha=0.6)
plt.xlabel('Age')
plt.ylabel('Treatment Response')
plt.title('Age vs Treatment Response by Treatment')
plt.legend()
plt.savefig(os.path.join(visualization_path, 'age_response_correlation.png'))
plt.close()

# Gender analysis
print("\n7. Gender analysis")
gender_response = df.groupby(['sex', 'treatment_name'])['treatment_response'].agg([
    'mean', 'std', 'count'
]).round(3)
print("\nResponse by gender and treatment:")
print(gender_response)

# Export summary report
print("\n8. Generating summary report")
with open('trial_analysis_summary.txt', 'w') as f:
    f.write("Clinical Trial Analysis Summary\n")
    f.write("============================\n\n")
    f.write("Treatment Statistics:\n")
    f.write(treatment_stats.to_string())
    f.write("\n\nCondition Analysis:\n")
    f.write(condition_analysis.to_string())
    f.write("\n\nStatistical Tests:\n")
    f.write(f"ANOVA p-value: {p_value:.4f}")

print("\nAnalysis complete! Check the visualization_assets folder for plots")
print("and trial_analysis_summary.txt for the complete report.")

conn.close()