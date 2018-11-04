import requests
from pairs import pairs
from config import key, account_id
import pprint

# print(pairs)

starting_currency = 'USD'

# Headers required by API
headers = {
    "Authorization": key
}

# Helper function to request API data


def send_request(url, headers):
    r = requests.get(url, headers=headers).json()
    return r


obj = {}

for pair in pairs:

    obj[pair] = {}

    for instrument in pair:

        instrument_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=6&price=M&granularity=S5".format(
            instrument)
        instrument_data = send_request(instrument_url, headers)
        name = instrument_data['instrument']
        rate = instrument_data['candles'][0]['mid']['c']

        obj[pair][instrument] = rate

pprint.pprint(obj)
