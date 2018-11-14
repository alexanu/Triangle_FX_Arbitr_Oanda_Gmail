from oandapyV20 import API
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.transactions as transactions
import oandapyV20.endpoints.pricing as pricing
import configparser
import requests
from random import randint

## Account
# r = accounts.AccountChanges(accountID)
# r = accounts.AccountConfiguration(accountID)
# r = accounts.AccountDetails(accountID)
# r = accounts.AccountInstruments(accountID, params='EUR_USD')
# r = accounts.AccountList()
# r = accounts.AccountSummary(accountID)

# Instrument
# r = instruments.InstrumentsCandles('EUR_USD')
# r = instruments.InstrumentsOrderBook('EUR_USD')
# r = instruments.InstrumentsPositionBook('EUR_USD')

# Orders
# r = orders.OrderCancel(accountID)
# r = orders.OrderClientExtensions(accountID)
# r = orders.OrderCreate(accountID, data)
# r = orders.OrderDetails(accountID)
# r = orders.OrderList(accountID)
# r = orders.OrderReplace(accountID)
# r = orders.Orders(accountID)
# r = orders.OrdersPending(accountID)

# Trades
# r = trades.TradeClientExtensions(accountID)
# r = trades.TradeClose(accountID)
# r = trades.TradeCRCDO(accountID)
# r = trades.TradeDetails(accountID)
# r = trades.Trades(accountID)
# r = trades.TradesList(accountID)

# Positions
# r = positions.OpenPositions(accountID)
# r = positions.PositionClose(accountID)
# r = positions.PositionDetails(accountID)
# r = positions.PositionList(accountID)
# r = positions.Positions(accountID)

# Transactions
# r = transactions.StreamTerminated()
# r = transactions.TransactionDetails(accountID)
# r = transactions.TransactionIDRange(accountID)
# r = transactions.TransactionList(accountID)
# r = transactions.Transactions(accountID)
# r = transactions.TransactionsSinceID(accountID)
# r = transactions.TransactionsStream(accountID)

# Pricing
# r = pricing.Pricing(accountID)
# r = pricing.PricingInfo(accountID, params='EUR_USD')
# r = pricing.PricingStream(accountID, params='EUR_USD')


class Oanda():
    config = configparser.ConfigParser()
    config.read('./config/oanda.ini')
    accountID = config['oanda']['account_id']
    access_token = config['oanda']['api_key']
    api = API(access_token=access_token)
    client = oandapyV20.API(access_token=access_token)
    headers = {
        # "Content-Type": "application/json",
        "Authorization": 'Bearer ' + str(access_token)
    }

    def __init__(self):
        pass

    def send_request(self, r):
        Oanda.client.request(r)
        return r.response

    def getPrice(self, instruments):
        return self.send_request(pricing.PricingInfo(Oanda.accountID, params={'instruments': instruments}))

    def getCurrentAsk(self, instruments):
        ask = self.send_request(pricing.PricingInfo(Oanda.accountID, params={'instruments': instruments}))['prices'][0]['asks'][0]['price']
        return float(ask)

    def getCurrentBid(self, instruments):
        bid = self.send_request(pricing.PricingInfo(Oanda.accountID, params={'instruments': instruments}))['prices'][0]['bids'][0]['price']
        return float(bid)

    def connectToStream(self, instruments):
        s = requests.Session()
        url = "https://stream-fxpractice.oanda.com/v3/accounts/{}/pricing/stream?instruments={}".format(Oanda.accountID, instruments)
        req = requests.Request('GET', url, headers=Oanda.headers)
        pre = req.prepare()
        resp = s.send(pre, stream=True, verify=True)
        return resp
    
    def placeMarketBuyOrder(self, instrument, units):
        data = {
            "order": {
                "instrument": instrument,
                "units": str(units),
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        return self.send_request(orders.OrderCreate(Oanda.accountID, data))

    def placeMarketSellOrder(self, instrument, units):
        data = {
            "order": {
                "instrument": instrument,
                "units": str(float(units) * -1),
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        return self.send_request(orders.OrderCreate(Oanda.accountID, data))
    
    def PickRandomPair(self, pair_type):
      pairs = {
        'major': ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CAD', 'USD_CHF', 'AUD_USD', 'NZD_USD'],
        'minor': ['EUR_GBP', 'EUR_CHF', 'EUR_CAD', 'EUR_AUD', 'EUR_NZD', 'EUR_JPY', 'GBP_JPY', 'CHF_JPY', 'CAD_JPY', 'AUD_JPY', 'NZD_JPY', 'GBP_CHF', 'GBP_AUD', 'GBP_CAD'],
        'exotic': ['EUR_TRY', 'USD_SEK', 'USD_NOK', 'USD_DKK', 'USD_ZAR', 'USD_HKD', 'USD_SGD']
      }
      length = len(pairs[pair_type]) - 1
      return pairs[pair_type][randint(0, length)]