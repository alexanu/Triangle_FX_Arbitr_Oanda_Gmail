#!/usr/bin/env python3

# Run the following bash command in the terminal to loop script
# while :; do ./Strategies/SimpleShort.py; sleep 60; done

import json
import sys
sys.path.append('/Users/troysmith/Code/TradingBots/Arb-Bot/Engines') 
from Oanda import Oanda
Oanda = Oanda()

# Ask the user for instrument and units to short
# pair = input('What instrument do you want to short? ')
# units = input('How many units of ' + pair + ' do you want to short? ')

pair = Oanda.PickRandomPair('major')
print(pair)
orderType = 'SHORT'
units = 100000

short_price = float(Oanda.placeMarketSellOrder(pair, units)['orderFillTransaction']['price'])
print(short_price)

## Connecting to pricing stream for instrument
response = Oanda.connectToStream(pair)

# This will run every price update
if response.status_code != 200:
    print(response.text)

for line in response.iter_lines(1):
    if line:
        try:
            line = line.decode('utf-8')
            msg = json.loads(line)
            instrument = msg['instrument']
            ask_price = float(msg['asks'][0]["price"])

            profit = short_price - ask_price

            print('Short Price(' + pair + '): ' + str(short_price))
            print('Current Ask Price (' + pair + '): ' + str(ask_price))
            print('Current Profit (if bought back): ', profit)

            # When profit reaches this threshold, buy back the instrument for the same units
            if profit > 0.005:
                print('🔥 PROFIT ALERT: ', short_price - ask_price, '🔥')
                print('Buying back', units, pair, '@', ask_price)
                Oanda.placeMarketBuyOrder(pair, units)
                quit()

            else:
                print('No profit')

            print('--------------------------------------------------------')

        except Exception as e:
            print("Caught exception: " + str(e))
            print('--------------------------------------------------------')
