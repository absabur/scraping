import os
import pandas as pd

# Get the current script directory
directory = os.getcwd()  # This sets the directory to the script's location

# List all Excel files in the directory
excel_files = [f for f in os.listdir(directory) if f.endswith(".xlsx") or f.endswith(".xls")]
# excel_files = ["1.xlsx", "2.xlsx", "3.xlsx", "4.xlsx"]

# List to store DataFrames
df_list = []

# Read all sheets from each Excel file
for file in excel_files:
    file_path = os.path.join(directory, file)
    xls = pd.ExcelFile(file_path)
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df["Source_File"] = file
        df["Sheet_Name"] = sheet
        df_list.append(df)

# Combine all DataFrames and remove duplicates
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
    
    # Save to a new Excel file (optional)
    combined_df.to_excel("combined.xlsx", index=False)
    
    print("Successfully combined all Excel files into 'combined.xlsx' without duplicates.")
else:
    print("No Excel files found in the directory.")
