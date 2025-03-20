import pandas as pd

# Load the main file and second file
main_df = pd.read_excel("main.xlsx")
second_df = pd.read_excel("second.xlsx")

# Define the common column name
key_column = "License Number"
unique_column = "License Number"

# Remove rows where the key column is empty
main_df = main_df.dropna(subset=[key_column])

# Merge the dataframes on the key column
merged_df = main_df.merge(second_df, on=key_column, how="left")

# Remove duplicates based on the key column, keeping the first occurrence
final_df = merged_df.drop_duplicates(subset=[unique_column], keep="first")

# Save the cleaned merged data to an Excel file
final_df.to_excel("merged_file.xlsx", index=False)

print("Merging and duplicate removal completed. Check 'merged_file.xlsx'.")
