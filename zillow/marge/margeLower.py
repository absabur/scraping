import pandas as pd

# Load Excel files
main_df = pd.read_excel("main.xlsx")
second_df = pd.read_excel("second.xlsx")

# Convert to lowercase for case-insensitive matching
main_df["EmailAddress_lower"] = main_df["EmailAddress"].str.lower()
second_df["EmailAddress_lower"] = second_df["EmailAddress"].str.lower()

# Merge, keeping all rows from main_df and only matching columns from second_df
merged_df = main_df.merge(second_df.drop(columns=["EmailAddress"]), on="EmailAddress_lower", how="left")

# Drop the temporary lowercase column
merged_df.drop(columns=["EmailAddress_lower"], inplace=True)

# Save the updated main Excel file
merged_df.to_excel("updated_main.xlsx", index=False)

print("Updated main.xlsx saved successfully.")
