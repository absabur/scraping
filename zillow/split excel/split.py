import pandas as pd
import numpy as np

# Load the Excel file
file_path = "large_file.xlsx"
df = pd.read_excel(file_path)

# Split the dataframe into 3 roughly equal parts
split_dfs = np.array_split(df, 3)

# Save each part as a new Excel file
for i, chunk in enumerate(split_dfs):
    chunk.to_excel(f"output_part_{i+1}.xlsx", index=False, engine="openpyxl")
    print(f"Saved output_part_{i+1}.xlsx")
