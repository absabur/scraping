from datetime import datetime, timedelta

# Excel serial date number
excel_date = 45722

# Excel's base date (1900 system) starts from 1899-12-30 in Python
base_date = datetime(1899, 12, 30)

# Convert to datetime
converted_date = base_date + timedelta(days=excel_date)

# Format to match "YYYY-MM-DD HH:MM:SS"
formatted_date = converted_date.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_date)  # Output: "2025-03-06 00:00:00"
