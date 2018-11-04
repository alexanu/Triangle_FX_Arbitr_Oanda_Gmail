from config import key, account_id
from pairs import pairs
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

# Opening result.txt file
myfile = open('results.txt', 'w')
pair_no = 0

# Initializing results object
obj = {}

# Function to get price for all possible instrument pairs
for pair in pairs:

    # Initializing current pair object
    obj[pair] = {}

    # Fetch data for each instrument
    for instrument in pair:
        instrument_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=6&price=M&granularity=S5".format(instrument)
        instrument_data = send_request(instrument_url, headers)
        name = instrument_data['instrument']
        rate = instrument_data['candles'][0]['mid']['c']

        # Add data to results object
        obj[pair][instrument] = rate
    
    # Calculate if arbitrage exist between the pairing
    profit = arb_calculator(obj[pair], starting_balance, starting_currency)
    profit_margin = (profit / starting_balance) * 100

    # Writing pair results to result file
    if profit != -starting_balance:
      myfile.write("%s, %s\n" %(pair_no, profit_margin))
      pair_no += 1

# Closing result file
myfile.close()