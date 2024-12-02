import pandas as pd
import json

def extract_unique_specs(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Initialize a dictionary to track unique categories and their specifications
    unique_specs = {}

    # Filter out rows where both 'Category' and 'Specification' are not null
    specs_group = df[df['Specification'].notnull()]

    # Group by category and extract unique specifications
    specs_by_category = specs_group.groupby('Category')
    for category, spec_group in specs_by_category:
        unique_specs[category] = []
        for _, spec_row in spec_group.iterrows():
            spec_key = spec_row['Specification']
            # Only append unique specifications
            if spec_key not in unique_specs[category]:
                unique_specs[category].append(spec_key)

    # Convert the dictionary to JSON
    return json.dumps(unique_specs, indent=4)

# Example usage
excel_file = 'all-mobile.xlsx'  # Replace with your Excel file path
unique_specs_json = extract_unique_specs(excel_file)

# Save the unique specs JSON to a file
with open('unique_specs.json', 'w') as json_file:
    json_file.write(unique_specs_json)

print("Unique category and specifications JSON file created successfully!")
