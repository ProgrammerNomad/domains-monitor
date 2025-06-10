import os
import json
import csv
from datetime import datetime
import pandas as pd

def load_technologies():
    """Load and display available technologies"""
    with open('data/technologies.json', 'r', encoding='utf-8') as f:
        tech_data = json.load(f)['technology']
    
    print("\nAvailable Technologies:")
    for i, tech in enumerate(tech_data, 1):
        print(f"{i}. {tech['name']} (Daily count: {tech['count_daily']})")
    
    return tech_data

def select_technology(tech_data):
    """Let user select a technology"""
    while True:
        try:
            choice = int(input("\nEnter technology number: ")) - 1
            if 0 <= choice < len(tech_data):
                return tech_data[choice]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def select_data_type(tech_name):
    """Let user select full or daily data"""
    files = {
        'full': f'data/technologies/{tech_name}.txt',
        'daily': f'data/technologies/{tech_name}_daily.txt'
    }
    
    available_types = []
    print("\nAvailable data types:")
    for data_type, filepath in files.items():
        if os.path.exists(filepath):
            available_types.append(data_type)
            print(f"- {data_type}")
    
    while True:
        choice = input("\nSelect data type (full/daily): ").lower()
        if choice in available_types:
            return choice, files[choice]
        print("Invalid selection. Please try again.")

def load_domain_list(filepath):
    """Load domains from technology file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def process_detailed_data(domains, tech_name, data_type):
    """Process the detailed CSV file and extract matching domains"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join('data', 'extracted', tech_name)
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{data_type}_{timestamp}.csv')
    detailed_file = 'data/detailed/domains-detailed.csv'
    
    print(f"\nProcessing detailed data for {tech_name}...")
    
    # Optimize chunk size for memory efficiency (adjust based on your RAM)
    chunk_size = 50000  # Smaller chunk size
    first_chunk = True
    total_matches = 0
    
    try:
        # Convert domains to set for faster lookups
        domain_set = set(domains)
        
        # Use iterator for memory efficient reading
        csv_iterator = pd.read_csv(
            detailed_file, 
            sep=';', 
            quotechar='"',
            chunksize=chunk_size,
            names=['domain', 'nameservers', 'ip', 'country', 
                  'tech1', 'tech2', 'tech3', 'tech4', 'tech5'],
            usecols=['domain', 'nameservers', 'ip', 'country'],  # Only load needed columns
            dtype={
                'domain': 'string',
                'nameservers': 'string',
                'ip': 'string',
                'country': 'string'
            }
        )
        
        for i, chunk in enumerate(csv_iterator, 1):
            # Filter rows where domain is in our target domains
            matched_rows = chunk[chunk['domain'].isin(domain_set)]
            
            if not matched_rows.empty:
                # Write to CSV
                matched_rows.to_csv(
                    output_file, 
                    mode='a' if not first_chunk else 'w',
                    header=first_chunk,
                    index=False,
                    sep=';',
                    quoting=csv.QUOTE_ALL
                )
                
                total_matches += len(matched_rows)
                first_chunk = False
                
            # Progress update
            if i % 20 == 0:  # Show progress every 20 chunks
                print(f"Processed {i * chunk_size:,} rows, found {total_matches:,} matches...")
                
            # Clear memory
            del chunk
            del matched_rows
            
    except Exception as e:
        print(f"Error processing file: {e}")
        return False
        
    print(f"\nProcessing complete!")
    print(f"Total matches found: {total_matches:,}")
    print(f"Extracted data saved to: {output_file}")
    return True

def main():
    # Load and select technology
    tech_data = load_technologies()
    selected_tech = select_technology(tech_data)
    
    # Select data type
    data_type, tech_file = select_data_type(selected_tech['name'])
    
    # Load domain list
    print(f"\nLoading domain list from {tech_file}...")
    domains = load_domain_list(tech_file)
    print(f"Loaded {len(domains)} domains")
    
    # Process detailed data
    process_detailed_data(domains, selected_tech['name'], data_type)

if __name__ == "__main__":
    main()