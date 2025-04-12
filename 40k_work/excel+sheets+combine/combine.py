import os
import pandas as pd
from glob import glob

# Set directory containing Excel files
directory = os.getcwd()  # This sets the directory to the script's location

# List all Excel files in the directory
excel_files = [f for f in os.listdir(directory) if f.endswith(".xlsx") or f.endswith(".xls")]

# Initialize empty list to store dataframes
all_dataframes = []

# Read each Excel file
for file in excel_files:
    # Get all sheet names
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names

    # Read all sheets and append to list
    for sheet in sheet_names:
        df = pd.read_excel(file, sheet_name=sheet)
        df['Source_File'] = file  # Optional: Add column to track source file
        df['Sheet_Name'] = sheet  # Optional: Add column to track sheet
        all_dataframes.append(df)

# Combine all dataframes
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Remove duplicates based on a specific column (e.g., 'ID'), keeping the first occurrence
column_to_check = "email"  # Change this to your actual column name
combined_df = combined_df[~combined_df.duplicated(subset=[column_to_check], keep="first")]

# Save the final DataFrame
combined_df.to_excel("combined_output.xlsx", index=False)
