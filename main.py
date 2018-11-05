from config import key, account_id
from pair_maker import pairs
from arb_calc import arb_calculator
import requests
import pprint

# Change this after you decide on which currency and how much to start with 
starting_currency = 'USD'
starting_balance = 1000

# Headers required for API
headers = {"Authorization": key}

# Helper function to request API data
def send_request(url, headers):
    r = requests.get(url, headers=headers).json()
    return r

# # Opening result.txt file
# myfile = open('results.txt', 'w')
# pair_no = 0

# Initializing results object
obj = {}

start_currency_pairs = []
for pair in pairs:
  for instrument in pair:
    if starting_currency in instrument and pair not in start_currency_pairs:
        start_currency_pairs.append(pair)


# Function to get price for all possible instrument pairs
for pair in start_currency_pairs:

    # Initializing current pair object
    obj[pair] = {}

    # Fetch data for each instrument
    for instrument in pair:
        obj[pair][instrument] = {}

        # Get bid data
        bid_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=1&price=B&granularity=S5".format(instrument)
        bid_data = send_request(bid_url, headers)
        pprint.pprint(bid_data)
        name = bid_data['instrument']
        bid_rate = float(bid_data['candles'][0]['bid']['c'])

        # Get ask data
        ask_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=1&price=A&granularity=S5".format(instrument)
        ask_data = send_request(ask_url, headers)
        pprint.pprint(ask_data)
        name = ask_data['instrument']
        ask_rate = float(ask_data['candles'][0]['ask']['c'])

        # Add data to results object
        obj[pair][instrument]['bid'] = bid_rate
        obj[pair][instrument]['ask'] = ask_rate
    
    pprint.pprint(obj[pair])

    # Calculate if arbitrage exist between the pairing
    arb_calculator(obj[pair], starting_balance, starting_currency)


# # Closing result file
# myfile.close()