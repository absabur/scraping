import pandas as pd
from PyPDF2 import PdfReader
import re

def simple_pdf_to_excel(pdf_path, excel_path):
    """
    Simple and reliable PDF to Excel conversion
    """
    print("Reading PDF...")
    reader = PdfReader(pdf_path)
    
    all_data = []
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip headers and page info
            if any(skip in line for skip in ['Repertorio Clipping', '/291', '=====', 'CED']):
                continue
                
            # Skip empty lines and column headers
            if not line or 'Tipo' in line and 'Plataforma' in line:
                continue
            
            # Split by multiple spaces (table data)
            parts = re.split(r'\s{2,}', line)
            
            if len(parts) >= 4:
                # Create record - adjust indices based on your data structure
                record = {
                    'Tipo': parts[0] if len(parts) > 0 else '',
                    'Plataforma': parts[1] if len(parts) > 1 else '',
                    'PublicationID': parts[2] if len(parts) > 2 else '',
                    'CedroCode': parts[3] if len(parts) > 3 else '',
                    'Editorial': parts[4] if len(parts) > 4 else '',
                    'Cabecera': parts[5] if len(parts) > 5 else '',
                    'URLs': parts[6] if len(parts) > 6 else '',
                    'Precios': ' '.join(parts[7:]) if len(parts) > 7 else ''
                }
                
                # Only add if it has basic required fields
                if record['PublicationID'] and record['Tipo']:
                    all_data.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    if df.empty:
        print("No data found! Please check the PDF structure.")
        return
    
    # Clean data
    df = df.dropna(how='all')
    
    # Save to Excel
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    print(f"Success! Created {excel_path} with {len(df)} records")
    print("\nFirst 5 records:")
    print(df.head().to_string())
    
    return df

# Run the conversion
if __name__ == "__main__":
    input_pdf = "repositorio-clipping.pdf"
    output_excel = "clipping_data.xlsx"
    
    try:
        result = simple_pdf_to_excel(input_pdf, output_excel)
        if result is not None:
            print(f"\nSummary:")
            print(f"Total records: {len(result)}")
            print(f"Types: {result['Tipo'].value_counts().to_dict()}")
            print(f"Platforms: {result['Plataforma'].value_counts().to_dict()}")
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure:")
        print("1. The PDF file exists in the same directory")
        print("2. The PDF is not password protected")
        print("3. You have installed required packages: pandas, openpyxl, PyPDF2")