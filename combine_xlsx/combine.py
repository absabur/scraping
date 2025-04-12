import os
import pandas as pd

# Get the current script directory
directory = os.getcwd()  # This sets the directory to the script's location

# List all Excel files in the directory
excel_files = [f for f in os.listdir(directory) if f.endswith((".xlsx", ".xls"))]

# List to store DataFrames
df_list = []

# Read all sheets from each Excel file
for file in excel_files:
    file_path = os.path.join(directory, file)
    
    try:
        # Determine engine based on file extension
        if file.endswith(".xls"):
            xls = pd.ExcelFile(file_path, engine="xlrd")
        else:
            xls = pd.ExcelFile(file_path, engine="openpyxl")
        
        for sheet in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Source_File"] = file
                df["Sheet_Name"] = sheet
                df_list.append(df)
            except Exception as e:
                print(f"Error reading sheet '{sheet}' in file '{file}': {e}")
    
    except Exception as e:
        print(f"Error opening file '{file}': {e}")

# Combine all DataFrames and remove duplicates
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
    combined_df.to_excel("combined.xlsx", index=False)
    print(f"Successfully combined {len(excel_files)} Excel files into 'combined.xlsx' with {len(combined_df)} rows.")
else:
    print("No valid Excel files found or all failed to load.")
