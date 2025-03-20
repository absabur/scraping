import pandas as pd

# Load the sheets
main_sheet = pd.read_excel('sh1.xlsx')
additional_sheet = pd.read_excel('sh2.xlsx')

# Ensure unique 'LINKEDIN' keys in both sheets
main_sheet = main_sheet.drop_duplicates(subset=['clean linkedin'])
additional_sheet = additional_sheet.drop_duplicates(subset=['clean linkedin'])

# Merge the sheets based on the 'LINKEDIN' column
combined_sheet = pd.merge(main_sheet, additional_sheet, on='clean linkedin', how='left')

# Remove any duplicates in the final combined sheet if necessary
combined_sheet = combined_sheet.drop_duplicates(subset=['clean linkedin'], keep='first')

# Save the combined sheet to a new file
combined_sheet.to_excel('combined_sheet.xlsx', index=False)

print("Sheets have been successfully combined without duplicates.")
