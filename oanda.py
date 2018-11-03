## Testing w/ Oanda REST-V20 API

from config import key, account_id
import requests
import json
import pprint
from data_init import pair_data

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


for instrument, values in pair_data.items():

  instrument_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=6&price=M&granularity=S5".format(instrument)
  instrument_data = send_request(instrument_url, headers)

  name = instrument_data['instrument']
  price = instrument_data['candles'][0]['mid']['c']

  pair_data[name]['exchange_data']['oanda'] = price


# pprint.pprint(pair_data)