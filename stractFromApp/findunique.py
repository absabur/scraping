import pandas as pd

# Load the Excel files
sheet1 = pd.read_excel("previous.xlsx")  # Replace "file1.xlsx" with the first file name
sheet2 = pd.read_excel("present.xlsx")  # Replace "file2.xlsx" with the second file name

# Specify the column for comparison
column_to_check = "namePostCompany"  # Replace with the column name you want to compare

# Find rows in sheet2 where the values in the specified column do not exist in sheet1
filtered_sheet2 = sheet2[~sheet2[column_to_check].isin(sheet1[column_to_check])]

# Save the filtered data to a new Excel file
filtered_sheet2.to_excel("final_sheet.xlsx", index=False)

print("Final sheet created with values from the second file that do not exist in the first file.")
