import pandas as pd

# Load Excel file
df = pd.read_excel("second.xlsx")

# Remove duplicate rows based on a specific column (e.g., 'Name'), keeping the first occurrence
df = df.drop_duplicates(subset=["License Number"], keep="first")

# Save the cleaned data to a new file
df.to_excel("secondf.xlsx", index=False)

print("Duplicate rows removed successfully and saved as 'cleaned_data.xlsx'.")
