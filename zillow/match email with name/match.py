import pandas as pd

# Load the Excel file
df = pd.read_excel("data.xlsx")

# Initialize an empty list to store match results
match_results = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Check if "First" or "Last" is in "email-1"
    if str(row["First"]).lower() in str(row["email-1"]).lower() or str(row["Last"]).lower() in str(row["email-2"]).lower():
        match_results.append("Match")
    else:
        match_results.append("Not Match")

# Assign the match results to a new column
df["Match_Status"] = match_results

# Save the updated DataFrame to a new Excel file
df.to_excel("updated_data.xlsx", index=False)

print("Comparison done and saved to updated_data.xlsx")
