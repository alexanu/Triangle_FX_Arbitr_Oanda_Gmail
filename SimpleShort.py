import pprint
import configparser
import threading

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.transactions as transactions
import oandapyV20.endpoints.pricing as pricing

config = configparser.ConfigParser()
config.read('./config/oanda.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

api = API(access_token=access_token)
client = oandapyV20.API(access_token=access_token)



# Short instrument
def short_instrument(instrument, units):
    data = {
        "order": {
            # "price": "1.2",
            # "timeInForce": "GTC",
            "instrument": instrument,
            "units": str(float(units) * -1),
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }

    r = orders.OrderCreate(accountID, data)
    client.request(r)
    # pprint.pprint(r.response)
    short_price = float(r.response['orderFillTransaction']['price'])
    # print(short_price)
    return short_price


# Detect if profit exists w/ current asking price
def profit_detector():

    global short_price
    global pair
    global units

    # To run this function every 5 seconds
    threading.Timer(0.5, profit_detector).start()

    params = {
        'instruments': pair
    }
    r = pricing.PricingInfo(accountID, params=params)
    client.request(r)
    # pprint.pprint(r.response)
    ask_price = float(r.response['prices'][0]['asks'][0]['price'])

    profit = short_price - ask_price
    # pips = profit / .0001

    print('Short Price: ', short_price)
    print('Current Ask Price: ', ask_price)
    print('Current Profit (if bought back): ', profit)

    if profit > 0.001:
        print('🔥 PROFIT ALERT: ', short_price - ask_price, '🔥')
        # print(pips, 'PIPS')
        print('Buying back', units, pair, '@', ask_price)
        data = {
            "order": {
                "price": str(ask_price),
                "timeInForce": "GTC",
                "instrument": pair,
                "units": str(units),
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        client.request(orders.OrderCreate(accountID, data))
        return

    else:
        print('No profit')

    print('--------------------------------------------------------')

pair = input('What instrument do you want to short? ')
units = input('How many units of ' + pair + ' do you want to short? ')
short_price = short_instrument(pair, units)
profit_detector()