# Transform Vehicle Data - Script Explanation

## Line-by-Line Explanation

### **IMPORTS (Lines 1-3)**
```python
import pandas as pd
import os
from datetime import datetime
```
- **`pandas`** - Library for data manipulation (reading/writing CSV, transformations)
- **`os`** - Operating system functions (file paths, directories) - imported but not used in this script
- **`datetime`** - For working with date/time objects - imported but not used here

**Why:** Pandas is essential for handling CSV files and data transformations efficiently.

---

### **FILE PATHS (Lines 5-7)**
```python
input_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_raw.csv'
output_file = r'd:\GitHub\test-vehicle-analytics\data\vehicle_signal_transformed.csv'
```
- Stores the location of input and output files
- `r` before the string = raw string (Windows backslashes treated literally)
- Variables make it easy to change paths without editing the whole script

**Why:** Easy to modify file locations in one place instead of throughout the code.

---

### **LOAD DATA (Lines 9-13)**
```python
print("Loading data from:", input_file)
df = pd.read_csv(input_file)

print(f"Original data shape: {df.shape}")
print(f"Original data info:\n{df.info()}\n")
```
- **`pd.read_csv()`** - Reads CSV file into a DataFrame (like an Excel table in Python)
- **`df.shape`** - Shows (rows, columns) - e.g., (30, 9) means 30 rows and 9 columns
- **`df.info()`** - Shows column names, data types, and missing values count

**Why:** Need to understand what data we're working with before transformation.

---

### **TRANSFORM 1: Convert event_time to Datetime (Lines 18-20)**
```python
df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
invalid_times = df[df['event_time'].isna()].shape[0]
print(f"  - Invalid event_time values: {invalid_times}")
```
- **`pd.to_datetime()`** - Converts text to datetime format (YYYY-MM-DD HH:MM:SS)
- **`errors='coerce'`** - If conversion fails, turns it into NaN (missing value) instead of crashing
- **`df[df['event_time'].isna()]`** - Finds rows where event_time is NaN
- **`.shape[0]`** - Counts how many rows have NaN

**Why:** Timestamps should be datetime objects for sorting and filtering. Coerce prevents errors on invalid data.

**Example:**
- Input: `"2024-12-01 08:00:00"` → Output: `Timestamp('2024-12-01 08:00:00')`
- Input: `"INVALID_TIME"` → Output: `NaN`

---

### **TRANSFORM 2: Convert ingestion_time (Lines 22)**
```python
df['ingestion_time'] = pd.to_datetime(df['ingestion_time'], errors='coerce')
```
Same as above - converts ingestion_time to datetime format.

**Why:** Ensures consistent data types for time-based operations.

---

### **TRANSFORM 3: Convert signal_value to Numeric (Lines 24-26)**
```python
df['signal_value'] = pd.to_numeric(df['signal_value'], errors='coerce')
missing_values = df[df['signal_value'].isna()].shape[0]
print(f"  - Missing/invalid signal_value: {missing_values}")
```
- **`pd.to_numeric()`** - Converts text/strings to numbers (integers or floats)
- Empty cells or non-numeric values become NaN
- Counts how many values are missing

**Why:** Signal values need to be numbers for calculations, analysis, and statistics.

**Example:**
- Input: `"12"` → Output: `12.0`
- Input: `""` (empty) → Output: `NaN`

---

### **TRANSFORM 4: Remove Invalid Rows (Lines 28-30)**
```python
df_cleaned = df.dropna(subset=['event_time'])
print(f"  - Rows removed due to invalid event_time: {df.shape[0] - df_cleaned.shape[0]}")
```
- **`dropna(subset=['event_time'])`** - Removes rows where event_time is NaN
- **`df_cleaned`** - New DataFrame without invalid rows
- Calculates how many rows were removed (original count - cleaned count)

**Why:** Rows with invalid timestamps are unreliable and shouldn't be in final data.

---

### **TRANSFORM 5: Fill Missing Signal Values (Lines 32-39)**
```python
for signal in df_cleaned['signal_name'].unique():
    mask = (df_cleaned['signal_name'] == signal) & (df_cleaned['signal_value'].isna())
    median_value = df_cleaned[df_cleaned['signal_name'] == signal]['signal_value'].median()
    if pd.notna(median_value):
        df_cleaned.loc[mask, 'signal_value'] = median_value
        print(f"  - Filled missing {signal} values with median: {median_value}")
```

**Line by line:**
- **`for signal in df_cleaned['signal_name'].unique():`** - Loop through each unique signal type (speed, soc, voltage, temp)
- **`mask = ...`** - Creates a boolean mask (True/False for each row) that identifies:
  - Rows where signal_name matches current signal AND
  - signal_value is NaN (missing)
- **`.median()`** - Calculates middle value of all existing values for that signal type
- **`if pd.notna(median_value):`** - Only fills if median exists (not all values are NaN)
- **`df_cleaned.loc[mask, 'signal_value'] = median_value`** - Fills the masked rows with median value

**Why:** Instead of deleting rows with missing values, we intelligently fill them with the median (middle value) of similar signals. This preserves more data.

**Example:**
- Signal: `speed`, existing values: `[0, 12, 35, 48, 60]`
- Median = 35
- If a speed value is missing, fill with 35

---

### **TRANSFORM 6: Add Derived Columns (Lines 41-42)**
```python
df_cleaned['date'] = df_cleaned['event_time'].dt.date
df_cleaned['hour'] = df_cleaned['event_time'].dt.hour
```
- **`.dt.date`** - Extracts just the date part (YYYY-MM-DD) from timestamp
- **`.dt.hour`** - Extracts just the hour (0-23) from timestamp

**Why:** These new columns make it easier to analyze data by date or time of day.

**Example:**
- Timestamp: `2024-12-01 08:30:00` → date: `2024-12-01`, hour: `8`

---

### **TRANSFORM 7: Sort Data (Lines 44)**
```python
df_cleaned = df_cleaned.sort_values(['vehicle_id', 'trip_id', 'event_time']).reset_index(drop=True)
```
- **`sort_values()`** - Orders rows by multiple columns (primary: vehicle_id, secondary: trip_id, tertiary: event_time)
- **`.reset_index(drop=True)`** - Resets row numbers after sorting (drops old index)

**Why:** Organized data is easier to read and analyze. Sorted by vehicle and time for chronological analysis.

---

### **CHECK TRANSFORMED DATA (Lines 46-47)**
```python
print(f"\nTransformed data shape: {df_cleaned.shape}")
print(f"Transformed data info:\n{df_cleaned.info()}\n")
```
Same as before - shows final data shape and column info to verify transformations worked.

---

### **SAVE TO CSV (Lines 49-56)**
```python
print(f"Saving transformed data to: {output_file}")
df_cleaned.to_csv(output_file, index=False)
print("✓ Transformation completed successfully!")
print(f"\nSummary:")
print(f"  Input file: {input_file}")
print(f"  Output file: {output_file}")
print(f"  Records processed: {df.shape[0]}")
print(f"  Records saved: {df_cleaned.shape[0]}")
```
- **`.to_csv()`** - Writes DataFrame to CSV file
- **`index=False`** - Don't save row numbers (index) in the file
- Prints summary showing input/output files and record counts

**Why:** Saves the cleaned data so you can use it in other tools or analyses.

---

## **Overall Flow**

```
1. Load raw data (30 rows)
   ↓
2. Convert data types (text → datetime, numeric)
   ↓
3. Identify missing/invalid values
   ↓
4. Remove bad rows (1 row removed)
   ↓
5. Fill missing values intelligently (median strategy)
   ↓
6. Add useful columns (date, hour)
   ↓
7. Sort for better organization
   ↓
8. Save cleaned data (29 rows)
```
