#!/usr/bin/env python3

"""
Strategy
Look at the 5-day moving average and trade from the other side
Buy if current price is below its moving average and Short if it is above
"""

# Imports
import pandas as pd
import numpy as np
import datetime
import pprint
import json
import sys
sys.path.append('/Users/troysmith/Code/AlgorithmicTradingBots/Engines')
from Oanda import Oanda
from Engine import Engine
Oanda = Oanda()
Engine = Engine()

# Get current positions
positions = Oanda.GetPositions()
positionObjList = positions['positions']
positionList = [position['instrument'] for position in positionObjList]

# Pick an instrument that there isnt an existing position for
# instrument = None
instrument = Oanda.PickRandomPair('all')
while instrument in positionList:
    instrument = Oanda.PickRandomPair('all')

# Calculate 5 day moving address for chosen instrument
SMA5 = Oanda.getSMA5(instrument)

# Get current prices for chosen instrument
current_ask = Oanda.getCurrentAsk(instrument)
current_bid = Oanda.getCurrentBid(instrument)

# Calculate units to trade
# account_summary = Oanda.GetAvailableBalance()
# nav = account_summary['account']['NAV']
# pprint.pprint(account_summary)
# units = nav
units = 100000

# Data visualization
date = str(datetime.datetime.now())[:10]
time = str(datetime.datetime.now().time())
data = np.array([[' ', 'Date', 'Time', 'Instrument', 'SMA5', 'Bid', 'Ask'],
                 [' ', date, time, instrument, SMA5, current_bid, current_ask]])

print(pd.DataFrame(data=data[1:, 1:],
                   index=data[1:, 0],
                   columns=data[0, 1:]))

# Choose take profit price
# take_profit = round(SMA5, 3)
take_profit_on_buy = round(current_ask * 1.05, 3)
take_profit_on_short = round(current_bid * 0.95, 3)

# If current ask price is lower than the SMA5, buy the pair
if current_ask < SMA5:
    data = {
        "order": {
            "instrument": instrument,
            "units": str(round(float(units), 0)),
            "takeProfitOnFill": {
                "price": take_profit_on_buy
            },
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    trade = Oanda.placeMarketBuyOrder(data)
    # trade_price = float(Oanda.placeMarketBuyOrder(data)['orderFillTransaction']['price'])
    # trade_type = 'LONG'


# If current bid price is higher than the SMA5, short the pair
if current_bid > SMA5:
    data = {
        "order": {
            "instrument": instrument,
            "units": str(round(float(units), 0) * -1),
            "takeProfitOnFill": {
                "price": take_profit_on_short
            },
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    trade = Oanda.placeMarketSellOrder(data)
    # trade_price = float(Oanda.placeMarketSellOrder(data)['orderFillTransaction']['price'])
    # trade_type = 'SHORT'

pprint.pprint(trade)

# Engine.EmailTradeDetails(trade)

# # Connecting to pricing stream for instrument
# response = Oanda.connectToStream(instrument)

# # This will run every price update
# if response.status_code != 200:
#     print(response.text)

# for line in response.iter_lines(1):
#     if line:
#         try:
#             line = line.decode('utf-8')
#             msg = json.loads(line)
#             date = str(datetime.datetime.now())[:10]
#             time = str(datetime.datetime.now().time())
#             instrument = msg['instrument']
#             bid_price = float(msg['bids'][0]["price"])
#             ask_price = float(msg['asks'][0]["price"])

#             # Data visualization
#             data = np.array([[' ', 'Date', 'Time', 'Instrument', 'Trade', 'Bid', 'Ask', 'SMA5'],
#                              [' ', date, time, instrument, trade_type + ' @ ' + str(round(trade_price, 5)), bid_price, ask_price, round(SMA5, 6)]])

#             print(pd.DataFrame(data=data[1:, 1:],
#                                index=data[1:, 0],
#                                columns=data[0, 1:]))

#             # When price crosses the SMA5, sell back the instrument for the same units
#             if bid_price > SMA5 and trade_type == 'LONG':
#                 Oanda.placeMarketSellOrder(instrument, units)
#                 print('Selling ' + instrument + ' @ ' + str(bid_price))
#                 quit()

#             # When price crosses the SMA5, buy back the instrument for the same units
#             if ask_price < SMA5 and trade_type == 'SHORT':
#                 Oanda.placeMarketBuyOrder(instrument, units)
#                 print('Buying ' + instrument + ' @ ' + str(ask_price))
#                 quit()

#             # print('Has not crossed SMA5 yet.')
#             print(
#                 '-------------------------------------------------------------------------------------')

#         except Exception as e:
#             print("Caught exception: " + str(e))
#             print(
#                 '-------------------------------------------------------------------------------------')
