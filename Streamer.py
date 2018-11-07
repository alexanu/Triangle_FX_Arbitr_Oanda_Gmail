from config import key, account_id
from ArbWrapper import ArbitrageWrapper
import pprint
import json

starting_balance = 1000
starting_currency = 'USD'
instrument_1 = 'EUR_USD'

arb = ArbitrageWrapper(starting_balance, starting_currency)

response = arb.connect_to_stream(instrument_1)

if response.status_code != 200:
  print(response.text)
  # return

for line in response.iter_lines(1):
    if line:
        try:
            line = line.decode('utf-8')
            msg = json.loads(line)
            bid_price = msg['bids'][0]["price"]
            ask_price = msg['asks'][0]["price"]
            print(instrument_1 + ' Bid: ', bid_price)
            print(instrument_1 + ' Ask: ', ask_price)
            print('-----------------------------------')

        except Exception as e:
            print("Caught exception when converting message into json\n" + str(e))
            # return

        # if "instrument" in msg or "tick" in msg:
        #     pprint.pprint(line)