import pandas as pd
import json

# Load both sheets by name or index
xls = pd.ExcelFile("input.xlsx")  # Replace with your file

# Read specific sheets (by name or index)
sheet1 = pd.read_excel(xls, sheet_name=0)  # First sheet
# sheet2 = pd.read_excel(xls, sheet_name=1)  # Second sheet

# Extract column 'AQ' from each sheet
column1 = sheet1['z_zillow_profile'].dropna().astype(str).tolist()
# column2 = sheet2['URL-href'].dropna().astype(str).tolist()

# Convert to JSON
json1 = json.dumps(column1, indent=2)
# json2 = json.dumps(column2, indent=2)

# Save both to separate files
with open("zillow2.json", "w") as f1:
    f1.write(json1)

# with open("sheet2_column_aq.json", "w") as f2:
#     f2.write(json2)

# Optional: print to console
print("Sheet 1 AQ column:")
print(json1)
# print("\nSheet 2 AQ column:")
# print(json2)
