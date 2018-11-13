from Engines.Oanda import Oanda
Oanda = Oanda()

pair = input('What instrument do you want to short? ')
units = input('How many units of ' + pair + ' do you want to short? ')

short_price = float(Oanda.placeMarketSellOrder(pair, units)['orderFillTransaction']['price'])
current_ask_price = Oanda.getCurrentAsk(pair)

loop = True

# Detect if profit exists w/ current asking price
while loop:

    current_ask_price = Oanda.getCurrentAsk(pair)

    profit = short_price - current_ask_price

    print('Short Price: ', short_price)
    print('Current Ask Price: ', current_ask_price)
    print('Current Profit (if bought back): ', profit)

    if profit > 0.0001:
        print('🔥 PROFIT ALERT: ', short_price - current_ask_price, '🔥')
        print('Buying back', units, pair, '@', current_ask_price)
        Oanda.placeMarketBuyOrder(pair, units)
        loop = False

    else:
        print('No profit')

    print('--------------------------------------------------------')