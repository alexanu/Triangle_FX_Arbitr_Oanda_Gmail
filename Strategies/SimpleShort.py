#!/usr/bin/env python3

# Run the following bash command in the terminal to loop script
# while :; do ./Strategies/SimpleShort.py; sleep 60; done

import pandas as pd
import numpy as np
import datetime

import json
import sys
sys.path.append('/Users/troysmith/Code/AlgorithmicTradingBots/Engines') 
from Oanda import Oanda
Oanda = Oanda()

# Ask the user for instrument and units to short
# pair = input('What instrument do you want to short? ')
# units = input('How many units of ' + pair + ' do you want to short? ')

pair = Oanda.PickRandomPair('major')
print(pair)
orderType = 'SHORT'
units = 10000

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
            date = str(datetime.datetime.now())[:10]
            time = str(datetime.datetime.now().time())
            instrument = msg['instrument']
            ask_price = float(msg['asks'][0]["price"])
            profit = short_price - ask_price

            # When profit reaches this threshold, buy back the instrument for the same units
            if profit > 0.005:
                result = '🔥PROFIT🔥'
                print('🔥 PROFIT ALERT: ', short_price - ask_price, '🔥')
                print('Buying back', units, pair, '@', ask_price)
                Oanda.placeMarketBuyOrder(pair, units)
                quit()

            else:
                result = 'No Profit'
                # print('No profit')

            # Data visualization
            data = np.array([[' ', 'Date', 'Time', 'Instrument', 'Short', 'Ask', 'Profit', 'Result'],
                            [' ' , date, time, instrument, short_price, ask_price, round(profit, 6), result]])

            print(pd.DataFrame(data=data[1:,1:],
                              index=data[1:,0],
                              columns=data[0,1:]))

            print('-------------------------------------------------------------------------------')

        except Exception as e:
            print("Caught exception: " + str(e))
            print('-------------------------------------------------------------------------------')