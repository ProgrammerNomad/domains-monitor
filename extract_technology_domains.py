import os
import json
import csv
from datetime import datetime
import time

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
    start_time = time.time()
    
    # Convert domains to set for faster lookups
    domain_set = set(domains)
    found_domains = set()
    total_matches = 0
    lines_processed = 0
    
    try:
        # Process input file and write matches immediately
        with open(detailed_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile, delimiter=';')
            writer = csv.writer(outfile, delimiter=',')
            
            for row in reader:
                lines_processed += 1
                
                if lines_processed % 1000000 == 0:  # Show progress every million lines
                    elapsed_time = time.time() - start_time
                    print(f"Processed {lines_processed:,} lines in {elapsed_time:.2f} seconds")
                    print(f"Found {total_matches:,} matches so far...")
                    print(f"Last saved match: {output_file}")
                
                if row[0].strip('"') in domain_set:
                    # Remove quotes and write immediately to file
                    cleaned_row = [field.strip('"') for field in row]
                    writer.writerow(cleaned_row)
                    outfile.flush()  # Force write to disk
                    
                    found_domains.add(row[0].strip('"'))
                    total_matches += 1
                    
                    # Stop if all domains are found
                    if len(found_domains) == len(domain_set):
                        print("\nAll domains found! Stopping search...")
                        break
    
    except Exception as e:
        print(f"Error processing file: {e}")
        print(f"Progress saved up to {total_matches} matches in: {output_file}")
        return False
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nProcessing complete!")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Lines processed: {lines_processed:,}")
    print(f"Total matches found: {total_matches:,}")
    print(f"Final file saved as: {output_file}")
    
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