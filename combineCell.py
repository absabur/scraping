import pandas as pd

excel_file_path = 'combine.xlsx'

df = pd.read_excel(excel_file_path)

employees = df.to_dict(orient='records')

for employee in employees:
    employee['search'] = f"{employee['combined']} {employee['text']}"

df = pd.DataFrame(employees)

excel_file_path = f'combined.xlsx'

df.to_excel(excel_file_path, index=False)
