## Testing w/ Oanda REST-V20 API
from config import *
import requests
import json
import pprint

# URL to receive all currency pairs listed on API
tradeable_instruments_url = "https://api-fxpractice.oanda.com/v3/accounts/101-001-9183876-001/instruments"

# Headers required by API
headers={
"Authorization": key
}

# Helper function to request API data
def send_request(url, headers):
  r = requests.get(url, headers=headers).json()
  return r

# Fetching all tadeable instrument data
all_tradeable_instruments = send_request(tradeable_instruments_url, headers)["instruments"]

# initializing the data object
pair_data = {}

# Loop to add instrument data to pair_data object
for instrument in all_tradeable_instruments:
  name = instrument["name"]
  pair_data[name] = {
    "currency_base": name[:3],
    "currency_quoted": name[4:],
    "exchange_data": {
      "sample_exchange": 'N/A',
      "oanda": 'N/A',
      "schwab": 'N/A',
      "eTrade": 'N/A',
      "Robinhood": 'N/A'
    }
  }

# pprint.pprint(pair_data)