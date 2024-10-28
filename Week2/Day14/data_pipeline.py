# data_pipeline.py - Complete end-to-end data analysis pipeline

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys
from pathlib import Path

# Add the Day12-13 directory to Python path
current_dir = Path(__file__).resolve().parent  # Gets Day14 directory
parent_dir = current_dir.parent  # Gets Week2 directory
day12_13_dir = parent_dir / 'Day12-13'
sys.path.append(str(day12_13_dir))

# Now we can import from our Day12-13 scripts
from data_cleaning import clean_basic, handle_missing_values, handle_invalid_values
from data_validation import ClinicalDataValidator
from feature_engineering import create_statistical_features


class ClinicalDataPipeline:
    def __init__(self):
        """Initialize the data analysis pipeline"""
        # Set up paths
        self.base_path = Path('pipeline_output')
        self.visualization_path = Path('30-Day-Data-Analysis') / 'visualization_assets'

        # Create necessary directories
        self.base_path.mkdir(exist_ok=True)
        self.visualization_path.mkdir(exist_ok=True)
        
        # Initialize components
        self.validator = ClinicalDataValidator()
        self.db_path = 'clinical_data.db'
        
        # Setup logging
        self.log = []
        
    def run_pipeline(self):
        """Execute the complete data analysis pipeline"""
        try:
            print("Starting Clinical Data Analysis Pipeline...")
            
            # 1. Data Collection
            print("\n1. Collecting data from multiple sources...")
            raw_data = self.collect_data()
            
            # 2. Data Cleaning
            print("\n2. Cleaning collected data...")
            cleaned_data = self.clean_data(raw_data)
            
            # 3. Data Validation
            print("\n3. Validating data quality...")
            validation_results = self.validate_data(cleaned_data)
            
            # 4. Feature Engineering
            print("\n4. Engineering features...")
            enriched_data = self.engineer_features(cleaned_data)
            
            # 5. Analysis
            print("\n5. Performing analysis...")
            analysis_results = self.analyze_data(enriched_data)
            
            # 6. Generate Reports
            print("\n6. Generating reports...")
            self.generate_reports(analysis_results, validation_results)
            
            print("\nPipeline completed successfully!")
            return True
            
        except Exception as e:
            print(f"\nError in pipeline: {str(e)}")
            self.log.append(f"Pipeline failed: {str(e)}")
            return False
    
    def collect_data(self):
        """Collect data from various sources"""
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        
        # Load different types of data
        try:
            # Patient demographics
            demographics = pd.read_sql("""
                SELECT * FROM patients
            """, conn)
            
            # Lab results
            lab_results = pd.read_sql("""
                SELECT * FROM lab_results
            """, conn)
            
            # Vital signs
            vital_signs = pd.read_sql("""
                SELECT * FROM vital_signs
            """, conn)
            
            conn.close()
            
            return {
                'demographics': demographics,
                'lab_results': lab_results,
                'vital_signs': vital_signs
            }
            
        except Exception as e:
            self.log.append(f"Data collection failed: {str(e)}")
            raise
    
    def clean_data(self, raw_data):
        """Clean and preprocess the data"""
        cleaned_data = {}
        
        for data_type, df in raw_data.items():
            # Basic cleaning
            df_cleaned = clean_basic(df)
            
            # Handle missing values
            df_cleaned = handle_missing_values(df_cleaned)
            
            # Handle invalid values
            df_cleaned = handle_invalid_values(df_cleaned)
            
            cleaned_data[data_type] = df_cleaned
            
            self.log.append(f"Cleaned {data_type}: {len(df)} -> {len(df_cleaned)} records")
        
        return cleaned_data
    
    def validate_data(self, cleaned_data):
        """Validate data quality"""
        validation_results = {}
        
        for data_type, df in cleaned_data.items():
            # Run validation checks
            violations = self.validator.validate_data(df)
            
            # Store results
            validation_results[data_type] = {
                'violations': violations,
                'summary': violations.sum().to_dict(),
                'total_records': len(df),
                'clean_records': len(df) - len(violations[violations.any(axis=1)])
            }
            
            self.log.append(f"Validated {data_type}: {validation_results[data_type]['clean_records']} clean records")
        
        return validation_results
    
    def engineer_features(self, cleaned_data):
        """Create derived features and combine datasets"""
        try:
            # Create patient summary features
            patient_features = pd.merge(
                cleaned_data['demographics'],
                cleaned_data['vital_signs'].groupby('patient_id').agg({
                    'heart_rate': ['mean', 'std'],
                    'systolic_bp': ['mean', 'std'],
                    'diastolic_bp': ['mean', 'std']
                }).round(2),
                on='patient_id'
            )
            
            # Add lab result features
            lab_features = cleaned_data['lab_results'].pivot_table(
                index='patient_id',
                columns='test_name',
                values='value',
                aggfunc=['mean', 'std']
            ).round(2)
            
            # Combine all features
            enriched_data = pd.merge(
                patient_features,
                lab_features,
                on='patient_id',
                how='left'
            )
            
            self.log.append(f"Created {enriched_data.shape[1]} features for {len(enriched_data)} patients")
            
            return enriched_data
            
        except Exception as e:
            self.log.append(f"Feature engineering failed: {str(e)}")
            raise
    
    def analyze_data(self, enriched_data):
        """Perform data analysis"""
        analysis_results = {}
        
        # Statistical analysis
        analysis_results['basic_stats'] = enriched_data.describe()
        
        # Correlation analysis
        numeric_cols = enriched_data.select_dtypes(include=[np.number]).columns
        analysis_results['correlations'] = enriched_data[numeric_cols].corr()
        
        # Create visualizations
        self._create_visualizations(enriched_data, analysis_results)
        
        return analysis_results
    
    def _create_visualizations(self, data, analysis_results):
        """Create analysis visualizations"""
        # Correlation heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(analysis_results['correlations'], 
                   cmap='coolwarm', center=0, annot=False)
        plt.title('Feature Correlations')
        plt.tight_layout()
        plt.savefig(self.visualization_path / 'correlation_heatmap.png')
        plt.close()
        
        # Distribution plots for key metrics
        key_metrics = ['heart_rate', 'systolic_bp', 'diastolic_bp']
        fig, axes = plt.subplots(1, len(key_metrics), figsize=(15, 5))
        
        for i, metric in enumerate(key_metrics):
            sns.histplot(data=data, x=f"{metric}_mean", ax=axes[i])
            axes[i].set_title(f'{metric} Distribution')
            
        plt.tight_layout()
        plt.savefig(self.visualization_path / 'metric_distributions.png')
        plt.close()
    
    def generate_reports(self, analysis_results, validation_results):
        """Generate final reports"""
        # Create summary report
        report_path = self.base_path / 'analysis_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("Clinical Data Analysis Report\n")
            f.write("===========================\n\n")
            
            # Data quality summary
            f.write("Data Quality Summary:\n")
            for data_type, results in validation_results.items():
                f.write(f"\n{data_type}:\n")
                f.write(f"- Total records: {results['total_records']}\n")
                f.write(f"- Clean records: {results['clean_records']}\n")
                f.write(f"- Data quality: {(results['clean_records']/results['total_records']*100):.1f}%\n")
            
            # Analysis summary
            f.write("\nBasic Statistics:\n")
            f.write(analysis_results['basic_stats'].to_string())
            
            # Processing log
            f.write("\n\nProcessing Log:\n")
            for log_entry in self.log:
                f.write(f"- {log_entry}\n")
        
        # Save detailed results
        analysis_results['basic_stats'].to_csv(self.base_path / 'statistical_summary.csv')
        analysis_results['correlations'].to_csv(self.base_path / 'correlation_matrix.csv')

def main():
    """Run the complete pipeline"""
    pipeline = ClinicalDataPipeline()
    success = pipeline.run_pipeline()
    
    if success:
        print("\nPipeline completed successfully!")
        print("Check pipeline_output directory for reports")
        print("and visualization_assets directory for plots.")
    else:
        print("\nPipeline failed. Check logs for details.")

if __name__ == "__main__":
    main()