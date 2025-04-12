import json
import math
import copy

# Load the large array from a JSON file
with open('zillow2.json', 'r') as f:
    big_array = json.load(f)

# Load your original scraper config
with open('zillow_scraper_config.json', 'r') as f:
    scraper_template = json.load(f)

# Split the array into chunks of 30
chunk_size = 95
total_chunks = math.ceil(len(big_array) / chunk_size)

for i in range(total_chunks):
    chunk = big_array[i*chunk_size:(i+1)*chunk_size]
    
    # Deep copy to avoid modifying the original template
    scraper_config = copy.deepcopy(scraper_template)
    
    # Update _id and startUrl
    scraper_id = f"zillow_3-3_{i+1}"
    scraper_config["_id"] = scraper_id
    scraper_config["startUrl"] = chunk

    # Save to a new JSON file
    with open(f'{scraper_id}.json', 'w') as out_file:
        json.dump(scraper_config, out_file, indent=2)

print(f"✅ Created {total_chunks} scraper files with updated _id and 30 URLs each.")
