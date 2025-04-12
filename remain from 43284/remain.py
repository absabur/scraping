import pandas as pd

# Load the Excel files
first_df = pd.read_excel("remainfinal.xlsx")
second_df = pd.read_excel("work.xlsx")

# Specify the column to compare (replace 'column_name' with the actual column)
column_name = 'email'

# Filter rows that are in first_df but not in second_df based on the column
remain_df = first_df[~first_df[column_name].isin(second_df[column_name])]

# Save the result to remain.xlsx
remain_df.to_excel("remainf.xlsx", index=False)

print("Filtered data saved to remain.xlsx")
