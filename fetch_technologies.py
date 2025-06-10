import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = os.getenv('BASE_URL')

# Define endpoint
ENDPOINT = f"{BASE_URL}/{TOKEN}/technology-list/json/"

def fetch_technologies():
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        # Make API request
        response = requests.get(ENDPOINT)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        technologies = response.json()
        
        # Use fixed filename
        filename = os.path.join(data_dir, 'technologies.json')
        
        # Save to file with pretty printing
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(technologies, f, indent=4)
            
        print(f"Technologies list saved to: {filename}")
        return technologies
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching technologies: {e}")
        return None

if __name__ == "__main__":
    fetch_technologies()