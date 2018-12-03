#!/usr/bin/env python3

"""
Strategy:
The Fibonacci ratios, 23.6%, 38.2%, and 61.8%, can be applied for time series analysis to find support level. 
Whenever the price moves substantially upwards or downwards, it usually tends to retrace back before it continues to move in the original direction. 
For example, if the stock price has moved from $200 to $250, then it is likely to retrace back to $230 before it continues to move upward. 
The retracement level of $230 is forecasted using the Fibonacci ratios.
"""

# Imports
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import json
import sys
sys.path.append('/Users/troysmith/Code/AlgorithmicTradingBots/Engines')
from Oanda import Oanda
Oanda = Oanda()


# instrument = Oanda.PickRandomPair('major')
instrument = 'USD_JPY'
units = 2000000
print(instrument)

candles = Oanda.getSMA2M(instrument)
prices = list(map(lambda candle: float(candle['mid']['c']), candles))
fig, ax = plt.subplots()
ax.plot(prices, color='black')

price_min = min(prices)
price_max = max(prices)

# Fibonacci Levels considering original trend as upward move
diff = price_max - price_min
level1 = price_max - 0.236 * diff
level2 = price_max - 0.382 * diff
level3 = price_max - 0.618 * diff

print("Level", "Price")
print("0 ", price_max)
print("0.236", level1)
print("0.382", level2)
print("0.618", level3)
print("1 ", price_min)

ax.axhspan(level1, price_min, alpha=0.4, color='lightsalmon')
ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod')
ax.axhspan(level3, level2, alpha=0.5, color='palegreen')
ax.axhspan(price_max, level3, alpha=0.5, color='powderblue')

plt.ylabel("Price")
plt.xlabel("Date")
plt.legend(loc=2)
plt.show()

# # current_ask = Oanda.getCurrentAsk(instrument)
# # current_bid = Oanda.getCurrentBid(instrument)

# # Data visualization
# date = str(datetime.datetime.now())[:10]
# time = str(datetime.datetime.now().time())
# data = np.array([[' ', 'Date', 'Time', 'Instrument', 'SMA5', 'Bid', 'Ask'],
#                  [' ', date, time, instrument, SMA5, current_bid, current_ask]])

# print(pd.DataFrame(data=data[1:, 1:],
#                    index=data[1:, 0],
#                    columns=data[0, 1:]))

# # If current ask price is lower than the SMA5, buy the pair
# if current_ask < SMA5:
#     trade_price = float(Oanda.placeMarketBuyOrder(
#         instrument, units)['orderFillTransaction']['price'])
#     trade_type = 'LONG'


# # If current bid price is higher than the SMA5, short the pair
# if current_bid > SMA5:
#     trade_price = float(Oanda.placeMarketSellOrder(
#         instrument, units)['orderFillTransaction']['price'])
#     trade_type = 'SHORT'


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
