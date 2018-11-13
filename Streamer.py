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

            # Get object with profitable triangles
            result = arb.arb_calculator(triangle_obj)
            # pprint.pprint(result)

            print('Arbitrage Detected')
            # print('BUY ' + str(units) + ' units of ' + str(pairing[x]) + ' @ ASK price of ' + str(price) + ' = ' + str(balance) + ' ' + str(currency))

            # Place an order for each step in the triangle
            for trade in result['trades']:
                # pprint.pprint(trade)
                resp = arb.place_limit_order(trade)
                pprint.pprint(resp.text)

            print(
                '-----------------------------------------------------------------------')

        except Exception as e:
            continue
            # print("Caught exception when converting message into json\n" + str(e))
            # return

        # if "instrument" in msg or "tick" in msg:
        #     pprint.pprint(line)
