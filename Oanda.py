from oandapyV20 import API
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.transactions as transactions
import oandapyV20.endpoints.pricing as pricing

import configparser
import oandapyV20

config = configparser.ConfigParser()
config.read('../config/config.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

api = API(access_token=access_token)
client = oandapyV20.API(access_token=access_token)

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


# client.request(r)
# pprint.pprint(r.response)