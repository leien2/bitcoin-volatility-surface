import requests
import json
import os
from datetime import datetime
import pandas as pd

# Deribit API credentials
API_KEY = "VoAzluxQ"
API_SECRET = "nKtJcddYm5r_Ec6ElAR02YGSxx7pURKKK9lUIEGhh9E"
# Deribit REST API URL
DERIBIT_API_URL = "https://www.deribit.com/api/v2"

# Directory to save data
DATA_DIR = "option_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_instruments(currency="BTC", kind="option"):
    """
    Get Bitcoin options data from Deribit
    """
    # Get a list of all option contracts
    url = f"{DERIBIT_API_URL}/public/get_book_summary_by_currency"
    params = {
        "currency": currency,
        "kind": kind
    }

    try:
        print(f"Getting {currency} {kind} contract list...")
        # Sending a GET request
        response = requests.get(url, params=params)
        # Check if the request was successful
        response.raise_for_status()  
        # Get JSON data
        data = response.json()
        
        return data['result']
    except Exception as e:
        print(f"Request failed: {e}")
        return None
        
        
        

def save_instruments(currency="BTC", kind="option"):
    """get and save Bitcoin options data from Deribit"""
    instruments_data = get_instruments(currency, kind)

    # create timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # save to JSON file
    json_file = f"{DATA_DIR}/{currency}_{kind}_instruments_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(instruments_data, f, indent=2)

    print(f"order book saved: JSON Format - {json_file}")

    # create CSV file
    cleaned_data = []
    for inst in instruments_data:
        cleaned_data.append({
            "instrument_name": inst["instrument_name"],
            "creation_timestamp": inst["creation_timestamp"],
            "mark_iv": inst["mark_iv"]
        })
    # create DataFrame
    instruments_df = pd.DataFrame(cleaned_data)
    
    # save to CSV
    csv_file = f"{DATA_DIR}/{currency}_{kind}_instruments_{timestamp}.csv"
    instruments_df.to_csv(csv_file, index=False)
    print(f"order book saved: CSV Format - {csv_file}")


if __name__ == "__main__":
    save_instruments(currency="BTC", kind="option")