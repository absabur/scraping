import pandas as pd
import re

# Load the Excel file
df = pd.read_excel("cleaned_data.xlsx")

# Define a function to extract emails using regex
def extract_email(text):
    # Email regex pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, str(text))
    return match.group(0) if match else None

# Define a function to extract phone numbers using regex
def extract_phone(text):
    # Phone number regex pattern (you can adjust it based on the format)
    phone_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}'
    match = re.search(phone_pattern, str(text))
    return match.group(0) if match else None

# Apply the functions to create new columns for email and phone
df['Email'] = df['html'].apply(extract_email)
df['Phone'] = df['html'].apply(extract_phone)

# Save the modified DataFrame to a new Excel file
df.to_excel('modified_file.xlsx', index=False)

print("Emails and phone numbers separated successfully.")
