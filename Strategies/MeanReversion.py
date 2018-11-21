#!/usr/local/bin python3

# Run the following bash command in the terminal to loop script
# while :; do ./Strategies/SimpleShort.py; sleep 60; done

# Strategy
# Look at the 5-day moving average and trade from the other side
# Buy if current price is below its moving average and Short if it is above

# Imports
import pandas as pd
import numpy as np
import datetime

import json
import sys
sys.path.append('/Users/troysmith/Code/AlgorithmicTradingBots/Engines')
from Oanda import Oanda
Oanda = Oanda()


# instrument = Oanda.PickRandomPair('major')
instrument = 'EUR_USD'
units = 100000
SMA5 = Oanda.getSMA5(instrument)
current_ask = Oanda.getCurrentAsk(instrument)
current_bid = Oanda.getCurrentBid(instrument)

# Data visualization
date = str(datetime.datetime.now())[:10]
time = str(datetime.datetime.now().time())
data = np.array([[' ', 'Date', 'Time', 'Instrument', 'SMA5', 'Bid', 'Ask'],
                 [' ', date, time, instrument, SMA5, current_bid, current_ask]])

print(pd.DataFrame(data=data[1:, 1:],
                   index=data[1:, 0],
                   columns=data[0, 1:]))

# If current ask price is lower than the SMA5, buy the pair
if current_ask < SMA5:
    Oanda.placeMarketBuyOrder(instrument, units)
    trade_type = 'LONG'


# If current bid price is higher than the SMA5, short the pair
if current_bid > SMA5:
    Oanda.placeMarketSellOrder(instrument, units)
    trade_type = 'SHORT'


# Connecting to pricing stream for instrument
response = Oanda.connectToStream(instrument)

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
            bid_price = float(msg['bids'][0]["price"])
            ask_price = float(msg['asks'][0]["price"])

            # Data visualization
            data = np.array([[' ', 'Date', 'Time', 'Instrument', 'Type', 'Bid', 'Ask', 'SMA5'],
                             [' ', date, time, instrument, trade_type, bid_price, ask_price, round(SMA5, 6)]])

            print(pd.DataFrame(data=data[1:, 1:],
                               index=data[1:, 0],
                               columns=data[0, 1:]))


            # When price crosses the SMA5, sell back the instrument for the same units
            if bid_price > SMA5 and trade_type == 'LONG':
                Oanda.placeMarketSellOrder(instrument, units)
                quit()

            # When price crosses the SMA5, buy back the instrument for the same units
            if ask_price < SMA5 and trade_type == 'SHORT':
                Oanda.placeMarketBuyOrder(instrument, units)
                quit()

            # print('Has not crossed SMA5 yet.')
            print('-------------------------------------------------------------------------------')

        except Exception as e:
            print("Caught exception: " + str(e))
            print(
                '-------------------------------------------------------------------------------')
