import pandas as pd
import os

# Define the directory containing the Excel files
directory = os.getcwd()  # Change this to your directory

# Define the common columns to keep
common_columns = ['Name', 'Email', 'PersonLinkedIn', 'CompanyName', 'Website', 'key1']  # Replace with your actual column names

# Initialize an empty list to store the filtered DataFrames
dfs = []

# Loop through all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx') and filename != 'combined_output.xlsx':
        # Load the Excel file
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)

        # Filter the DataFrame to keep only the common columns
        filtered_df = df[common_columns]

        # Append the filtered DataFrame to the list
        dfs.append(filtered_df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new Excel file
combined_df.to_excel('combined_output.xlsx', index=False)
