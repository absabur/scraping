import pandas as pd

# Load the specific sheet from the Excel file
excel_path = 'input.xlsx'
sheet_name = '33478 all running'  # Change this to the name or index of your target sheet
df = pd.read_excel(excel_path, sheet_name=sheet_name)

# Calculate the size of each split
split_size = len(df) // 3

# Split the DataFrame into 3 parts
df1 = df.iloc[:split_size]
df2 = df.iloc[split_size:2*split_size]
df3 = df.iloc[2*split_size:]

# Save each part to a new Excel file
df1.to_excel('part1.xlsx', index=False)
df2.to_excel('part2.xlsx', index=False)
df3.to_excel('part3.xlsx', index=False)
