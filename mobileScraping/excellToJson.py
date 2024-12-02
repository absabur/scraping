import pandas as pd
import json

# Your list of dictionaries
brands = [
    {"_id": "671c14ed7343984e7b0748b1", "name": "Apple"},
    {"_id": "671c14ed7343984e7b0748b2", "name": "Xiaomi"},
    {"_id": "671c14ed7343984e7b0748b3", "name": "Oppo"},
    {"_id": "671c14ed7343984e7b0748b4", "name": "Samsung"},
    {"_id": "671c14ed7343984e7b0748b5", "name": "Vivo"},
    {"_id": "671c14ed7343984e7b0748b6", "name": "Realme"},
    {"_id": "671c14ed7343984e7b0748b7", "name": "Infinix"},
    {"_id": "671c14ed7343984e7b0748b8", "name": "Tecno"},
    {"_id": "671c14ed7343984e7b0748b9", "name": "Google"},
    {"_id": "671c14ed7343984e7b0748ba", "name": "Walton"},
    {"_id": "671c14ed7343984e7b0748bb", "name": "OnePlus"},
    {"_id": "671c14ed7343984e7b0748bc", "name": "Itel"},
    {"_id": "671c14ed7343984e7b0748bd", "name": "Honor"},
    {"_id": "671c14ed7343984e7b0748be", "name": "Motorola"},
    {"_id": "671c14ed7343984e7b0748bf", "name": "Nokia"},
    {"_id": "671c14ed7343984e7b0748c0", "name": "Nothing"},
    {"_id": "671c14ed7343984e7b0748c1", "name": "Symphony"},
    {"_id": "671c14ed7343984e7b0748c2", "name": "Asus"},
    {"_id": "671c14ed7343984e7b0748c3", "name": "Benco"},
    {"_id": "671c14ed7343984e7b0748c4", "name": "Helio"},
    {"_id": "671c14ed7343984e7b0748c5", "name": "ZTE"},
    {"_id": "671c14ed7343984e7b0748c6", "name": "Meizu"},
    {"_id": "671c14ed7343984e7b0748c7", "name": "Huawei"},
    {"_id": "671c14ed7343984e7b0748c8", "name": "HTC"},
    {"_id": "671c14ed7343984e7b0748c9", "name": "Lava"},
    {"_id": "671c14ed7343984e7b0748ca", "name": "Sony"},
    {"_id": "671c14ed7343984e7b0748cb", "name": "Lenovo"},
    {"_id": "671c14ed7343984e7b0748cc", "name": "Maximus"},
    {"_id": "671c14ed7343984e7b0748cd", "name": "TECNO"},
    {"_id": "671c14ed7343984e7b0748ce", "name": "TCL"},
    {"_id": "671c14ed7343984e7b0748cf", "name": "LG"},
    {"_id": "671c14ed7343984e7b0748d0", "name": "HMD"},
    {"_id": "671c14ed7343984e7b0748d1", "name": "Doogee"},
    {"_id": "671c14ed7343984e7b0748d2", "name": "Micromax"},
    {"_id": "671c14ed7343984e7b0748d3", "name": "Umidigi"},
    {"_id": "671c14ed7343984e7b0748d4", "name": "We"},
    {"_id": "671c14ed7343984e7b0748d5", "name": "Coolpad"},
    {"_id": "671c14ed7343984e7b0748d6", "name": "Nio"},
    {"_id": "671c14ed7343984e7b0748d7", "name": "Panasonic"},
    {"_id": "671c14ed7343984e7b0748d8", "name": "Alcatel"},
    {"_id": "671c14ed7343984e7b0748d9", "name": "Allview"},
    {"_id": "671c14ed7343984e7b0748da", "name": "WE"},
    {"_id": "671c14ed7343984e7b0748db", "name": "Oneplus"},
    {"_id": "671c14ed7343984e7b0748dc", "name": "OnePlus 2"},
    {"_id": "671c14ed7343984e7b0748dd", "name": "LAVA"},
    {"_id": "671c14ed7343984e7b0748de", "name": "WE X2"},
    {"_id": "671c14ed7343984e7b0748df", "name": "Okapia"},
    {"_id": "671c14ed7343984e7b0748e0", "name": "Mycell"},
    {"_id": "671c14ed7343984e7b0748e1", "name": "maximus"},
    {"_id": "671c14ed7343984e7b0748e2", "name": "Microsoft"},
    {"_id": "671c14ed7343984e7b0748e3", "name": "Ulefone"},
    {"_id": "671c14ed7343984e7b0748e4", "name": "Wiko"},
    {"_id": "671c14ed7343984e7b0748e5", "name": "Blackview"},
    {"_id": "671c14ed7343984e7b0748e6", "name": "FreeYond"},
    {"_id": "671c14ed7343984e7b0748e7", "name": "Kingstar"},
    {"_id": "671c14ed7343984e7b0748e8", "name": "Cubot"},
    {"_id": "671c14ed7343984e7b0748e9", "name": "DOOGEE"},
    {"_id": "671c14ed7343984e7b0748ea", "name": "Celkon"},
    {"_id": "671c14ed7343984e7b0748eb", "name": "Bengal"},
    {"_id": "671c14ed7343984e7b0748ec", "name": "Oukitel"},
    {"_id": "671c14ed7343984e7b0748ed", "name": "Oscal"},
]

def find_brand(brand_name):
    # Iterate through the list and find the brand
    for brand in brands:
        if brand['name'].lower() == brand_name.lower():  # Case insensitive comparison
            return brand  # Return the entire dictionary if found
    return None  # Return None if not found


def excel_to_json(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Print column names for debugging
    print("Columns in the Excel file:", df.columns.tolist())

    mobile_list = []
    
    for name, group in df.groupby('Mobile Name'):
        mobile_data = {
            "name": name,
            "slug": group['URL'].iloc[0].split('/')[-1],
            "price": [],
            "specifications": [],  # Changed to 'specifications' to match your JSON structure
            # "ViewImage": [],
            # "ColorImage": [],
            "brand": {
                "id": "",
                "value": ""
            }
        }

        # Add prices to mobile_data
        for _, row in group[group['Price'].notnull()].iterrows():
            mobile_data['price'].append({
                "varient": row['Variant'],
                "price": row['Price'],
                "status": row['Status']
            })

        # Group specifications by category and handle Brand separately
        specs_group = group[group['Specification'].notnull()]
        specs_by_category = specs_group.groupby('Category')
        
        for category, spec_group in specs_by_category:
            specs_list = []
            for _, spec_row in spec_group.iterrows():
                if spec_row['Specification'] == 'Brand':
                    # Assign brand information directly to mobile_data
                    mobile_data['brand'] = {
                        "id": find_brand(spec_row['Value'])["_id"],  # Assuming specId corresponds to the brand ID
                        "value": spec_row['Value']
                    }
                else:
                    # Handle other specifications
                    filter_values = []
                    if pd.notnull(spec_row['filterId']) and pd.notnull(spec_row['FilterValue']):
                        filter_values.append({
                            "filterId": spec_row['filterId'],
                            "filterValue": spec_row['FilterValue']
                        })
                    specs_list.append({
                        "specKeyId": spec_row['specId'],
                        "specKey": spec_row['Specification'],
                        "value": spec_row['Value'],
                        "filterValues": filter_values
                    })
            mobile_data['specifications'].append({
                "categoryId": spec_group['categoryId'].iloc[0],
                "categoryValue": category,
                "specs": specs_list
            })

        # Collect image paths
        
        # view_images = group[group['ImageType'] == 'View Image']['ImagePath'].tolist()
        # mobile_data['ViewImage'] = view_images

        # color_images = group[group['ImageType'] == 'Color Image']['ImagePath'].tolist()
        # mobile_data['ColorImage'] = color_images

        mobile_list.append(mobile_data)

    return json.dumps(mobile_list, indent=4)

# Example usage
excel_file = 'new.xlsx'  # Replace with your Excel file path
json_data = excel_to_json(excel_file)

# Save JSON to a file
with open('all-mobile.json', 'w') as json_file:
    json_file.write(json_data)

print("JSON file created successfully!")
