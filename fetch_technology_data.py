import os
import json
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = os.getenv('BASE_URL')

def load_technologies():
    """Load the list of technologies from technologies.json"""
    with open('data/technologies.json', 'r', encoding='utf-8') as f:
        return json.load(f)['technology']

def download_technology_data(tech_name):
    """Download data for a specific technology"""
    tech_dir = os.path.join('data', 'technologies')
    os.makedirs(tech_dir, exist_ok=True)
    
    endpoint = f"{BASE_URL}/{TOKEN}/technology/{tech_name}/list/text/"
    filename = os.path.join(tech_dir, f'{tech_name}.txt')
    
    try:
        print(f"Downloading {tech_name}...")
        response = requests.get(endpoint)
        response.raise_for_status()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved: {filename}")
        
        # Sleep to avoid hitting rate limits
        time.sleep(1)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {tech_name}: {e}")
        return False

def main():
    technologies = load_technologies()
    success_count = 0
    failed_count = 0
    
    for tech in technologies:
        if download_technology_data(tech['name']):
            success_count += 1
        else:
            failed_count += 1
        
        # Also download daily data if available
        if tech['count_daily'] != "0":
            daily_name = f"{tech['name']}_daily"
            if download_technology_data(daily_name):
                success_count += 1
            else:
                failed_count += 1
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded: {success_count}")
    print(f"Failed downloads: {failed_count}")

if __name__ == "__main__":
    main()