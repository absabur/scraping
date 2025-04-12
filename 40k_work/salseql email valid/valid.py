import pandas as pd

# Load the Excel file
df = pd.read_excel("input.xlsx")

# Initialize a list to store valid emails
valid_emails = []
invalid_emails = []

# Iterate through each row
for _, row in df.iterrows():
    valid_email = None
    for i in range(1, 7):  # Assuming email1 to email34
        email_col = f"email{i}"
        status_col = f"email_status{i}"
        if row.get(status_col) == "Valid":  # Check if email status is valid
            valid_email = row.get(email_col)
            break  # Stop at the first valid email
    valid_emails.append(valid_email)
for _, row in df.iterrows():
    valid_email = None
    for i in range(1, 8):  # Assuming email1 to email34
        email_col = f"email{i}"
        status_col = f"email_status{i}"
        if row.get(status_col) == "Unverifiable":  # Check if email status is valid
            valid_email = row.get(email_col)
            break  # Stop at the first valid email
    invalid_emails.append(valid_email)

# Add the new column to the DataFrame
df["valid_email"] = valid_emails
df["invalid_email"] = invalid_emails

# Save to a new file
df.to_excel("filtered_emails.xlsx", index=False)
