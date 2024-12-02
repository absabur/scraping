import json
import requests
import math

# Helper function to replace NaN values
def replace_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, dict):
        return {k: replace_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan(i) for i in obj]
    return obj

# Load JSON data from a file
with open('all-mobile.json') as f:
    data = json.load(f)

# Replace NaN values in data
data = replace_nan(data)

# Define variables
url = 'http://127.0.0.1:8000/api/phone/new'
chunk_size = 1
count = 1

# Send data in chunks
for i in range(0, len(data), chunk_size):
    # if count == 2:
    #     break
    
    if len(data[i]['price']) == 0:
        continue
    
    chunk = data[i:i+chunk_size]

    try:
        response = requests.post(url, json=chunk)
        
        # Check and print response details
        if response.status_code == 200:
            print(f'Successfully Item {count}')
        else:
            print(f'Failed to send chunk {count}: {response.status_code}, {response.text}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending chunk {count}: {e}")

    count += 1
