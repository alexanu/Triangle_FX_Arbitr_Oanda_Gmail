from config import key, account_id
from ArbWrapper import ArbitrageWrapper
import pprint
import json

# Inputs
starting_balance = 1000
starting_currency = 'USD'
instrument_1 = 'EUR_USD'
instrument_2 = 'EUR_GBP'
instrument_3 = 'GBP_USD'

instruments = instrument_1 + ',' + instrument_2 + ',' + instrument_3

arb = ArbitrageWrapper(starting_balance, starting_currency)

response = arb.connect_to_stream(instruments)

triangle_obj = {
  instrument_1: {},
  instrument_2: {},
  instrument_3: {}
}


total_profit = 0

if response.status_code != 200:
  print(response.text)
  # return

for line in response.iter_lines(1):
    if line:
        try:
            line = line.decode('utf-8')
            msg = json.loads(line)
            instrument = msg['instrument']
            bid_price = msg['bids'][0]["price"]
            ask_price = msg['asks'][0]["price"]

            if instrument == instrument_1:
              triangle_obj[instrument_1] = {
                'bid': float(bid_price),
                'ask': float(ask_price)
              }
            elif instrument == instrument_2:
              triangle_obj[instrument_2] = {
                'bid': float(bid_price),
                'ask': float(ask_price)
              }
            elif instrument == instrument_3:
              triangle_obj[instrument_3] = {
                'bid': float(bid_price),
                'ask': float(ask_price)
              }
            pprint.pprint(triangle_obj)
            print(instrument + ' Bid: ', bid_price)
            print(instrument + ' Ask: ', ask_price)
            total_profit += arb.arb_calculator(triangle_obj)
            print('TOTAL PROFIT: ', total_profit)
            print('-----------------------------------------------------------------------')


        except Exception as e:
            continue
            # print("Caught exception when converting message into json\n" + str(e))
            # return

        # if "instrument" in msg or "tick" in msg:
        #     pprint.pprint(line)