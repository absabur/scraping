import pandas as pd

# Load both sheets from a single Excel file
file_path = "1filemain.xlsx"  # Change this to your actual file name
main_df = pd.read_excel(file_path, sheet_name="again fb(6487)")  # First sheet
second_df = pd.read_excel(file_path, sheet_name="mail FB")  # Second sheet

# Define the common column
key_column = "clean FB"

# Remove rows where the key column is empty in main_df
main_df = main_df.dropna(subset=[key_column])

# Merge the two DataFrames on the key column
merged_df = main_df.merge(second_df, on=key_column, how="left")

# Save the result to a new Excel file
merged_df.to_excel("merged_file.xlsx", index=False)

print("Merging of sheets completed. Check 'merged_file.xlsx'.")
