import pandas as pd

# Load the main file and second file
main_df = pd.read_excel("main.xlsx")
second_df = pd.read_excel("second.xlsx")

# Define the common column name
key_column = "ID"

# Separate rows with and without key_column
with_key = main_df[main_df[key_column].notna()]
without_key = main_df[main_df[key_column].isna()]

# Merge only rows with key_column
merged_with_key = with_key.merge(second_df, on=key_column, how="left")

# Combine merged rows and those without key_column
final_df = pd.concat([merged_with_key, without_key], ignore_index=True)

# Save the final merged data
final_df.to_excel("merged_file.xlsx", index=False)

print("Merging completed, including rows without key_column.")
