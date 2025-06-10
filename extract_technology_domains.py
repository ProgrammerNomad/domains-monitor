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
    output_dir = os.path.join('data', 'extracted', tech_name)
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{data_type}.csv')
    detailed_file = 'data/detailed/domains-detailed.csv'
    
    print(f"\nProcessing detailed data for {tech_name}...")
    
    # Convert domains to set for faster lookups
    domain_set = set(domains)
    found_domains = set()
    total_matches = 0
    
    try:
        # Open output file
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            
            # Process input file
            with open(detailed_file, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter=';')
                
                # Write each matching row
                for row in reader:
                    if row[0].strip('"') in domain_set:
                        # Remove quotes and write with comma delimiter
                        cleaned_row = [field.strip('"') for field in row]
                        writer.writerow(cleaned_row)
                        found_domains.add(row[0].strip('"'))
                        total_matches += 1
                        
                        # Progress update
                        if total_matches % 100 == 0:
                            print(f"Found {total_matches} matches...")
                        
                        # Stop if all domains are found
                        if len(found_domains) == len(domain_set):
                            print("All domains found! Stopping search...")
                            break
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return False
    
    print(f"\nProcessing complete!")
    print(f"Total matches found: {total_matches}")
    print(f"Extracted data saved to: {output_file}")
    
    # Report any missing domains
    missing_domains = domain_set - found_domains
    if missing_domains:
        print(f"\nWarning: {len(missing_domains)} domains were not found in the detailed data")
        
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