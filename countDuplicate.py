import pandas as pd

# Paths to input and output files
input_file_path = '1900+.xlsx'  # Replace with your input file path
output_file_path = 'output_with_counts.xlsx'  # Replace with your desired output file path
column_to_check = 'Website'  # Replace with the actual column name

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file_path)

# Calculate the count of each value in the specified column
count_series = df[column_to_check].value_counts()

# Create a DataFrame from the count series
count_df = count_series.reset_index()
count_df.columns = [column_to_check, 'Count']

# Merge the count DataFrame with the original DataFrame to keep only one instance of each value
merged_df = pd.merge(count_df, df.drop_duplicates(subset=[column_to_check]), on=column_to_check, how='left')

# Write the merged DataFrame to a new Excel file
merged_df.to_excel(output_file_path, index=False)

print(f"Output file with counts has been saved as {output_file_path}.")
