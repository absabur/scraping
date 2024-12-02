import json
import pandas as pd
from pandas import json_normalize

# Load the JSON file
with open('all-mobile.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Normalize JSON data (this works well with nested structures)
df = json_normalize(data)

# Save the dataframe to an Excel file
output_file = 'all-mobile.xlsx'
df.to_excel(output_file, index=False)

print(f"Data has been successfully converted to {output_file}")
