import pandas as pd

# Replace 'sheet1.xlsx' and 'sheet2.xlsx' with the path to your actual files
# If your data is in CSV format, you can use pd.read_csv instead
main_sheet = pd.read_excel('sh1.xlsx')
additional_sheet = pd.read_excel('sh2.xlsx')

# Merge the sheets based on the 'email' column
combined_sheet = pd.merge(main_sheet, additional_sheet, on='name', how='left')

# Save the combined sheet to a new file
combined_sheet.to_excel('combined_sheet.xlsx', index=False)

print("Sheets have been successfully combined.")