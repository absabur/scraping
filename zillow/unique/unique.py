import pandas as pd

# Load the first and second Excel files
df1 = pd.read_excel("file1.xlsx")  # First Excel file
df2 = pd.read_excel("file2.xlsx")  # Second Excel file

# Specify the column name for comparison
column_name = "License Number"

# Remove rows from df1 where column_name values exist in df2
df1_filtered = df1[~df1[column_name].isin(df2[column_name])]

# Save the filtered data to a new Excel file
df1_filtered.to_excel("filtered_file.xlsx", index=False)

print("Filtered file saved as 'filtered_file.xlsx'")
