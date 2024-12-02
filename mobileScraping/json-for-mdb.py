# import pandas as pd
# import json

# # Load the Excel file
# excel_file = 'specs.xlsx'  # Update this to your Excel file path
# df = pd.read_excel(excel_file)

# # Keep only rows with unique 'Specification' values

# df = df[df['Specification'].notna() & (df['Specification'] != '')]

# df_unique = df.drop_duplicates(subset=['categoryId', 'Specification'])

# # Convert the DataFrame to JSON format based on unique 'Specification'
# json_output = []
# for _, row in df_unique.iterrows():
#     json_object = {
#         "name": row["Specification"],
#         "categoryId": { "$oid": f"{row["categoryId"]}" },
#         "categoryIdValue": row["Category"],
#         "placeholder": row["Value"]
#     }
#     json_output.append(json_object)

# # Output JSON to a file or print
# output_file = 'specs.json'
# with open(output_file, 'w') as f:
#     json.dump(json_output, f, indent=4)

# print(f"JSON saved to {output_file}")

















# import pandas as pd
# import json

# # Paths to files
# excel_file = 'specs.xlsx'  # Original Excel file
# json_file = 'specs.json'  # JSON file with _id values

# # Load Excel file into DataFrame
# df = pd.read_excel(excel_file)

# # Load JSON data
# with open(json_file, 'r') as f:
#     data = json.load(f)

# # Create a dictionary to map (categoryId, Specification) pairs to _id
# id_mapping = {(item["categoryId"], item["name"]): item["_id"] for item in data}

# # Create a new column 'specId' by mapping (categoryId, Specification) pairs
# df['specId'] = df.apply(lambda row: id_mapping.get((row['categoryId'], row['Specification'])), axis=1)

# # Save back to the same Excel file
# df.to_excel(excel_file, index=False)

# print(f"Updated Excel file saved as {excel_file}")










# import pandas as pd
# import json

# # Load the Excel file
# excel_file = 'specs.xlsx'  # Update this to your Excel file path
# df = pd.read_excel(excel_file)

# # Remove rows with empty FilterValue
# df = df[df['FilterValue'].notna() & (df['FilterValue'] != '')]

# # Keep all rows and filter duplicates based on 'FilterValue' and 'specId'
# df_unique = df.drop_duplicates(subset=['FilterValue', 'specId'])

# # Convert the DataFrame to JSON format
# json_output = []
# for _, row in df_unique.iterrows():
#     json_object = {
#         "categoryId": {"$oid": f"{row["categoryId"]}"},
#         "categoryValue": row["Category"],
#         "specId": {"$oid": f"{row["specId"]}"},
#         "specValue": row["Specification"],  # Verify if this is correct
#         "value": row["FilterValue"],
#     }
#     json_output.append(json_object)

# # Output JSON to a file or print
# output_file = 'filters.json'
# with open(output_file, 'w') as f:
#     json.dump(json_output, f, indent=4)

# print(f"JSON saved to {output_file}")






import pandas as pd
import json

# Paths to files
excel_file = 'specs.xlsx'  # Original Excel file
json_file = 'filters.json'  # JSON file with _id values

# Load Excel file into DataFrame
df = pd.read_excel(excel_file)

# Load JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# Create a dictionary to map (categoryId, Specification) pairs to _id
id_mapping = {(item["specId"], item["value"]): item["_id"] for item in data}

# Create a new column 'specId' by mapping (categoryId, Specification) pairs
df['filterId'] = df.apply(lambda row: id_mapping.get((row['specId'], row['FilterValue'])), axis=1)

# Save back to the same Excel file
df.to_excel('new.xlsx', index=False)

print(f"Updated Excel file saved as {excel_file}")