import pandas as pd

# Load the main file and second file
main_df = pd.read_excel("main_file.xlsx")
second_df = pd.read_excel("second_file.xlsx")

# Define the common column name (change 'KeyColumn' to the actual column name)
key_column = "zillow_profile"

# Merge the dataframes on the key column
merged_df = main_df.merge(second_df, on=key_column, how="left")

# Save the merged data back to an Excel file
merged_df.to_excel("merged_file.xlsx", index=False)


print("Merging completed and saved as 'merged_file.xlsx'.")
