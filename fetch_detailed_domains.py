import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = os.getenv('BASE_URL')

def fetch_detailed_domains():
    """Download full detailed domain data in zip format"""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'detailed')
    os.makedirs(data_dir, exist_ok=True)
    
    # Construct endpoint URL for full detailed list
    endpoint = f"{BASE_URL}/{TOKEN}/get-detailed/full/list/zip/"
    
    try:
        print("Downloading full detailed domain data...")
        response = requests.get(endpoint, stream=True)
        response.raise_for_status()
        
        # Define filepath
        filepath = os.path.join(data_dir, 'detailed_full.zip')
        
        # Write response content to file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Successfully downloaded: {filepath}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading detailed data: {e}")
        return False

if __name__ == "__main__":
    fetch_detailed_domains()