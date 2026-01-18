# Vehicle Signal Data Transformation

This notebook performs data transformation on raw vehicle signal data:
- Validates and converts datetime fields
- Handles missing and invalid values
- Creates derived columns
- Produces cleaned and transformed dataset

## 1. Import Required Libraries

```python
import pandas as pd
import os
from datetime import datetime

print("Libraries imported successfully!")
```

## 2. Define File Paths

```python
# Define file paths
input_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_raw.csv'
output_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_transformed.csv'

print(f"Input file: {input_file}")
print(f"Output file: {output_file}")
```

## 3. Load the Raw Data

```python
# Load the CSV file
print("Loading data from:", input_file)
df = pd.read_csv(input_file)

print(f"\nOriginal data shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
```

## 4. Examine Data Information

```python
# Display data info
print(f"Data Info:")
print(df.info())

print(f"\nData Description:")
print(df.describe())
```

## 5. Convert Data Types and Handle Invalid Values

```python
print("Applying transformations...\n")

# 1. Handle invalid event_time values
df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
invalid_times = df[df['event_time'].isna()].shape[0]
print(f"  ✓ Invalid event_time values: {invalid_times}")

# 2. Convert ingestion_time to datetime
df['ingestion_time'] = pd.to_datetime(df['ingestion_time'], errors='coerce')
print(f"  ✓ Converted ingestion_time to datetime")

# 3. Convert signal_value to numeric, handling empty/invalid values
df['signal_value'] = pd.to_numeric(df['signal_value'], errors='coerce')
missing_values = df[df['signal_value'].isna()].shape[0]
print(f"  ✓ Missing/invalid signal_value: {missing_values}")
```

## 6. Remove Invalid Records

```python
# 4. Remove rows with invalid event_time
df_cleaned = df.dropna(subset=['event_time'])
rows_removed = df.shape[0] - df_cleaned.shape[0]
print(f"  ✓ Rows removed due to invalid event_time: {rows_removed}")
print(f"\nData shape after cleaning: {df_cleaned.shape}")
```

## 7. Fill Missing Signal Values

```python
# 5. Fill missing signal values with median by signal_name
print("\nFilling missing signal values with median by signal_name:")
for signal in df_cleaned['signal_name'].unique():
    mask = (df_cleaned['signal_name'] == signal) & (df_cleaned['signal_value'].isna())
    median_value = df_cleaned[df_cleaned['signal_name'] == signal]['signal_value'].median()
    if pd.notna(median_value):
        df_cleaned.loc[mask, 'signal_value'] = median_value
        print(f"  ✓ Filled missing {signal} values with median: {median_value}")
```

## 8. Create Derived Columns

```python
# 6. Add derived columns
df_cleaned['date'] = df_cleaned['event_time'].dt.date
df_cleaned['hour'] = df_cleaned['event_time'].dt.hour

print("✓ Added derived columns: date, hour")
print(f"\nSample of new columns:")
print(df_cleaned[['event_time', 'date', 'hour']].head())
```

## 9. Sort and Organize Data

```python
# 7. Sort by vehicle_id, trip_id, and event_time
df_cleaned = df_cleaned.sort_values(['vehicle_id', 'trip_id', 'event_time']).reset_index(drop=True)

print("✓ Sorted data by vehicle_id, trip_id, and event_time")
print(f"\nFirst few rows of cleaned data:")
print(df_cleaned.head())
```

## 10. Review Transformed Data

```python
print(f"\nTransformed data shape: {df_cleaned.shape}")
print(f"\nData Info:")
print(df_cleaned.info())

print(f"\nData Description:")
print(df_cleaned.describe())
```

## 11. Save Transformed Data

```python
# Save the transformed data
print(f"Saving transformed data to: {output_file}")
df_cleaned.to_csv(output_file, index=False)
print("✓ Transformation completed successfully!")
```

## 12. Summary Report

```python
print(f"\n{'='*60}")
print("TRANSFORMATION SUMMARY")
print(f"{'='*60}")
print(f"  Input file: {input_file}")
print(f"  Output file: {output_file}")
print(f"  Records processed: {df.shape[0]}")
print(f"  Records saved: {df_cleaned.shape[0]}")
print(f"  Records removed: {df.shape[0] - df_cleaned.shape[0]}")
print(f"\n  Columns in output: {list(df_cleaned.columns)}")
print(f"{'='*60}")
```

Here's what the notebook includes:

1. Introduction - Overview of the transformation steps
2. Import Libraries - Pandas, os, and datetime
3. Define Paths - File paths for input/output
4. Load Data - Read the raw CSV file
5. Data Inspection - View info and descriptive statistics
6. Type Conversion - Convert datetime and numeric fields
7. Data Cleaning - Remove invalid records
8. Fill Missing Values - Use median by signal name
9. Derived Columns - Add date and hour columns
10. Sort Data - Organize by vehicle_id, trip_id, and event_time
11. Review Results - Display transformed data info
12. Save Output - Export to CSV
13. Summary Report - Final statistics
