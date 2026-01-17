import pandas as pd
import os
from datetime import datetime

# Define file paths
input_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_raw.csv'
output_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_transformed.csv'

# Load the CSV file
print("Loading data from:", input_file)
df = pd.read_csv(input_file)

print(f"Original data shape: {df.shape}")
print(f"Original data info:\n{df.info()}\n")

# Perform transformations
print("Applying transformations...")

# 1. Handle invalid event_time values
df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
invalid_times = df[df['event_time'].isna()].shape[0]
print(f"  - Invalid event_time values: {invalid_times}")

# 2. Convert ingestion_time to datetime
df['ingestion_time'] = pd.to_datetime(df['ingestion_time'], errors='coerce')

# 3. Convert signal_value to numeric, handling empty/invalid values
df['signal_value'] = pd.to_numeric(df['signal_value'], errors='coerce')
missing_values = df[df['signal_value'].isna()].shape[0]
print(f"  - Missing/invalid signal_value: {missing_values}")

# 4. Remove rows with invalid event_time
df_cleaned = df.dropna(subset=['event_time'])
print(f"  - Rows removed due to invalid event_time: {df.shape[0] - df_cleaned.shape[0]}")

# 5. Fill missing signal values with median by signal_name
for signal in df_cleaned['signal_name'].unique():
    mask = (df_cleaned['signal_name'] == signal) & (df_cleaned['signal_value'].isna())
    median_value = df_cleaned[df_cleaned['signal_name'] == signal]['signal_value'].median()
    if pd.notna(median_value):
        df_cleaned.loc[mask, 'signal_value'] = median_value
        print(f"  - Filled missing {signal} values with median: {median_value}")

# 6. Add derived columns
df_cleaned['date'] = df_cleaned['event_time'].dt.date
df_cleaned['hour'] = df_cleaned['event_time'].dt.hour

# 7. Sort by vehicle_id, trip_id, and event_time
df_cleaned = df_cleaned.sort_values(['vehicle_id', 'trip_id', 'event_time']).reset_index(drop=True)

print(f"\nTransformed data shape: {df_cleaned.shape}")
print(f"Transformed data info:\n{df_cleaned.info()}\n")

# Save the transformed data
print(f"Saving transformed data to: {output_file}")
df_cleaned.to_csv(output_file, index=False)
print("✓ Transformation completed successfully!")
print(f"\nSummary:")
print(f"  Input file: {input_file}")
print(f"  Output file: {output_file}")
print(f"  Records processed: {df.shape[0]}")
print(f"  Records saved: {df_cleaned.shape[0]}")
