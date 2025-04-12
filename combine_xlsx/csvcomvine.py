import os
import pandas as pd

directory = os.getcwd()
csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]
df_list = []

for file in csv_files:
    file_path = os.path.join(directory, file)
    
    try:
        # Try UTF-8 first
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            # If UTF-8 fails, fallback to Windows-1252
            df = pd.read_csv(file_path, encoding="cp1252")
        
        df["Source_File"] = file
        df_list.append(df)

    except Exception as e:
        print(f"Error reading file '{file}': {e}")

if df_list:
    combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
    combined_df.to_csv("combined.csv", index=False)
    print(f"Successfully combined {len(csv_files)} CSV files into 'combined.csv' with {len(combined_df)} rows.")
else:
    print("No valid CSV files found or all failed to load.")
