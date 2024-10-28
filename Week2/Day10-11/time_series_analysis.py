# time_series_analysis.py - Working with temporal patient data
# This script demonstrates analysis of time-series medical data, specifically focusing on
# patient vital signs monitoring over time. Such analysis is crucial in clinical settings
# for detecting trends, anomalies, and patterns in patient health data.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Set up the visualization directory in the root folder
# We need to go up two levels from our current location (Week2/Day10-11)
visualization_path = os.path.join('30-Day-Data-Analysis','visualization_assets')
os.makedirs(visualization_path, exist_ok=True)

print("1. Creating sample patient monitoring data")

# Set random seed for reproducibility
np.random.seed(42)

# Generate a sequence of dates for our time series
# We'll create hourly measurements over 30 days
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(hours=i) for i in range(24*30)]  # 30 days of hourly data

# Create sample patient IDs
n_patients = 5
patients = [f'P{i:03d}' for i in range(n_patients)]

# Generate synthetic vital signs data
# This simulates continuous patient monitoring data including:
# - Body temperature (normally around 37°C)
# - Heart rate (normally around 75 bpm)
# - Blood pressure (normally around 120 mmHg systolic)
vital_signs_data = []
for patient in patients:
    # Generate baseline values for each patient
    # Each patient has their own "normal" values that fluctuate around a personal baseline
    baseline_temp = np.random.normal(37.0, 0.2)  # Normal body temperature with slight variation
    baseline_hr = np.random.normal(75, 5)        # Normal heart rate with variation
    baseline_bp = np.random.normal(120, 5)       # Normal blood pressure with variation
    
    for date in dates:
        # Add circadian rhythm (daily cycle) and random variation
        # Most vital signs follow a daily pattern influenced by sleep/wake cycles
        hour = date.hour
        daily_cycle = np.sin(2 * np.pi * hour / 24)  # Creates a sinusoidal pattern over 24 hours
        
        # Generate measurements with daily cycles and random noise
        temp = baseline_temp + 0.1 * daily_cycle + np.random.normal(0, 0.1)
        hr = baseline_hr + 5 * daily_cycle + np.random.normal(0, 2)
        bp = baseline_bp + 3 * daily_cycle + np.random.normal(0, 2)
        
        # Record the measurements
        vital_signs_data.append({
            'timestamp': date,
            'patient_id': patient,
            'temperature': temp,
            'heart_rate': hr,
            'blood_pressure': bp,
            # Most measurements are routine, some are emergency checks
            'measurement_type': np.random.choice(['routine', 'emergency'], p=[0.9, 0.1])
        })

# Create DataFrame and set the timestamp as index
# This enables time-based operations and selections
df = pd.DataFrame(vital_signs_data)
df.set_index('timestamp', inplace=True)

print("\n2. Basic time series operations")

# Resample data to hourly averages
# This helps smooth out noise and reduce data volume while maintaining trends
hourly_avg = df.groupby('patient_id').resample('H').mean()
print("\nHourly averages:")
print(hourly_avg.head())

# Calculate rolling means using 24-hour window
# Rolling means help identify trends while smoothing out short-term fluctuations
rolling_window = 24  # 24-hour window for daily averages
rolling_means = df.groupby('patient_id').rolling(window=rolling_window).mean()
print("\nRolling means (24-hour window):")
print(rolling_means.head())

print("\n3. Time-based analysis")

# Analyze daily patterns in vital signs
# This helps identify normal circadian rhythms and deviations
daily_patterns = df.groupby([df.index.hour, 'patient_id']).mean()
print("\nDaily patterns:")
print(daily_patterns.head())

# Visualize daily temperature patterns
plt.figure(figsize=(12, 6))
for patient in patients:
    patient_data = daily_patterns.xs(patient, level=1)['temperature']
    plt.plot(patient_data.index, patient_data.values, label=f'Patient {patient}')
plt.title('Daily Temperature Patterns by Patient')
plt.xlabel('Hour of Day')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(visualization_path, 'daily_temperature_patterns.png'))
plt.close()

print("\n4. Detecting anomalies")

def detect_anomalies(group, window=24, threshold=2):
    """
    Detect anomalies in vital signs using rolling statistics
    
    Parameters:
    - group: time series data for a single vital sign
    - window: number of hours to include in rolling statistics (default: 24 hours)
    - threshold: number of standard deviations to consider anomalous (default: 2)
    
    This approach identifies values that deviate significantly from recent trends,
    which could indicate medical issues requiring attention.
    """
    rolling_mean = group.rolling(window=window).mean()
    rolling_std = group.rolling(window=window).std()
    
    # Calculate z-scores relative to rolling statistics
    z_scores = (group - rolling_mean) / rolling_std
    return abs(z_scores) > threshold

# Detect temperature anomalies
temp_anomalies = df.groupby('patient_id')['temperature'].apply(detect_anomalies)
print("\nDetected anomalies:")
print(f"Total anomalies found: {temp_anomalies.sum()}")

print("\n5. Advanced time series operations")

# Calculate rate of change in vital signs
# Rapid changes can indicate acute medical issues
df['temp_rate_of_change'] = df.groupby('patient_id')['temperature'].diff()
df['hr_rate_of_change'] = df.groupby('patient_id')['heart_rate'].diff()

# Identify periods of rapid change that might require medical attention
rapid_changes = df[
    (abs(df['temp_rate_of_change']) > 0.5) |  # Significant temperature change
    (abs(df['hr_rate_of_change']) > 10)       # Significant heart rate change
]
print("\nPeriods of rapid change:")
print(rapid_changes.head())

# Create comprehensive visualization of vital signs for a single patient
patient_id = patients[0]
patient_data = df[df['patient_id'] == patient_id]

# Create a three-panel plot showing all vital signs
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Plot temperature
ax1.plot(patient_data.index, patient_data['temperature'])
ax1.set_ylabel('Temperature (°C)')
ax1.set_title(f'Vital Signs for {patient_id}')
ax1.grid(True)

# Plot heart rate
ax2.plot(patient_data.index, patient_data['heart_rate'])
ax2.set_ylabel('Heart Rate (bpm)')
ax2.grid(True)

# Plot blood pressure
ax3.plot(patient_data.index, patient_data['blood_pressure'])
ax3.set_ylabel('Blood Pressure (mmHg)')
ax3.set_xlabel('Time')
ax3.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(visualization_path, 'patient_vital_signs.png'))
plt.close()

print("\n6. Time window analysis")

# Analyze vital signs over different time windows
# This helps identify patterns at different time scales
windows = ['1H', '6H', '12H', '24H']
stats_by_window = {}

for window in windows:
    stats_by_window[window] = df.groupby('patient_id').resample(window).agg({
        'temperature': ['mean', 'std', 'min', 'max'],
        'heart_rate': ['mean', 'std', 'min', 'max'],
        'blood_pressure': ['mean', 'std', 'min', 'max']
    })

print("\nStatistics for different time windows:")
print(stats_by_window['24H'].head())

# Export results for further analysis
print("\n7. Exporting results")

# Create results directory
results_dir = 'time_series_results'
os.makedirs(results_dir, exist_ok=True)

# Save summary statistics for each time window
for window, stats in stats_by_window.items():
    stats.to_csv(os.path.join(results_dir, f'stats_{window}.csv'))

# Save anomaly data for follow-up investigation
temp_anomalies.to_csv(os.path.join(results_dir, 'temperature_anomalies.csv'))

print("\nTime series analysis complete! Check the visualization_assets folder for plots")
print("and time_series_results directory for detailed statistics.")