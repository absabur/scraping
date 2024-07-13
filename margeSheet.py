import pandas as pd
from fuzzywuzzy import process

# Function to match and merge dataframes based on a common column using fuzzy matching
def fuzzy_merge(df1, df2, key1, key2, threshold=90, limit=1):
    # Create a new column for the best match and the score
    df1['best_match'] = df1[key1].apply(lambda x: process.extractOne(x, df2[key2], score_cutoff=threshold))
    
    # Extract matched values and scores from the tuples
    df1['best_match_name'] = df1['best_match'].apply(lambda x: x[0] if x else None)
    df1['best_match_score'] = df1['best_match'].apply(lambda x: x[1] if x else None)
    
    # Drop the temporary 'best_match' column
    df1.drop(columns=['best_match'], inplace=True)
    
    # Merge dataframes based on the best match names
    merged_df = pd.merge(df1, df2, left_on='best_match_name', right_on=key2, how='left')
    
    return merged_df

# Read the two sheets
df1 = pd.read_excel('sheet1.xlsx')
df2 = pd.read_excel('sheet2.xlsx')

# Common column names (adjust as needed)
common_column_df1 = 'name'
common_column_df2 = 'name'

# Perform fuzzy matching and merge
merged_df = fuzzy_merge(df1, df2, common_column_df1, common_column_df2)

# Filter out rows where 'specific_column' has missing values
filtered_df = merged_df.dropna(subset=['HonorsAndAwards1'])

# Save the combined and filtered dataframe to a new Excel file
filtered_df.to_excel('combined_filtered.xlsx', index=False)

print("Combined and filtered dataframe saved to 'combined_filtered.xlsx'")








































# import pandas as pd

# def retain_first_line(file_path, columns_to_process, output_file):
#     # Load the Excel file
#     df = pd.read_excel(file_path)

#     # Process the specified columns
#     for column in columns_to_process:
#         if column in df.columns:
#             df[column] = df[column].apply(lambda x: str(x).split('\n')[0] if pd.notnull(x) else x)

#     # Save the modified DataFrame to a new Excel file
#     df.to_excel(output_file, index=False)

# # Specify the path to your input Excel file
# input_file = 'input_file.xlsx'

# # Specify the columns to process (list of column names)
# columns_to_retain_first_line = ['HonorsAndAwards1', 'HonorsAndAwards2', 'HonorsAndAwards3', 'HonorsAndAwards4', 'HonorsAndAwards5']

# # Specify the path to the output Excel file
# output_file = 'output_file.xlsx'

# # Call the function to process the file
# retain_first_line(input_file, columns_to_retain_first_line, output_file)

# print(f"Processed file saved as {output_file}")
