import pandas as pd

# Load the Excel files
before = pd.read_excel("before.xlsx")
after = pd.read_excel("after.xlsx")

# Specify the column to compare (change 'column_name' to your actual column)
column_name = "License Number"  # Change this to match your column name

# Find rows in 'before' that are NOT in 'after' based on the column
remain = before[~before[column_name].isin(after[column_name])]

# Save the remaining rows to a new Excel file
remain.to_excel("remain.xlsx", index=False)

print("Remain file created successfully: remain.xlsx")
