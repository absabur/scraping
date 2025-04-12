import pandas as pd
import json

# Step 1: Read the Excel file and extract a specific column
file_path = 'input.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Extract the column you want (assuming the column name is 'ColumnName')
column_data = df['zillow_profile'].tolist()  # Convert the column to a list

# Step 2: Convert the column data into a JSON file
data_dict = {
    'original_array': column_data
}

# Save the data to a JSON file
with open('column_data.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

# Step 3: Split the array into 5 smaller arrays
def split_array(arr, num_parts):
    # Split the array into smaller chunks (approximately equal size)
    avg_len = len(arr) // num_parts
    return [arr[i:i + avg_len] for i in range(0, len(arr), avg_len)]

# Split the column data into 5 arrays
split_arrays = split_array(column_data, 3)

# Step 4: Save the split arrays into a JSON file
split_data_dict = {
    'split_arrays': split_arrays
}

with open('split_column_data.json', 'w') as json_file:
    json.dump(split_data_dict, json_file, indent=4)

print("JSON files created successfully!")
