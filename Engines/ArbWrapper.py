from config import *
import requests
import json
import pprint
import itertools
import pprint


class ArbitrageWrapper:
    # Headers required by API
    headers = {
        "Content-Type": "application/json",
        "Authorization": key
    }
    environment = "demo"  # Replace this 'live' if you wish to connect to the live environment

    def __init__(self, starting_balance, starting_currency):
        self.starting_balance = starting_balance
        self.starting_currency = starting_currency
        print('Attempting to find arbitrage')
        print('Balance: ' + str(starting_balance) + ' ' + starting_currency)

    def send_request(self, url, headers):
        r = requests.get(url, headers=headers).json()
        return r

    def account_positions(self):
        """
        Environment                 Description 
        fxTrade (Live)              The live (real money) environment 
        fxTrade Practice (Demo)     The demo (simulated money) environment 
        """
        domainDict = {'live': 'stream-fxtrade.oanda.com',
                      'demo': 'stream-fxpractice.oanda.com'}
        domain = domainDict[ArbitrageWrapper.environment]
        try:
            s = requests.Session()
            url = "https://" + domain + \
                "/v3/accounts/{}/positions".format(account_id)
            # params = {'instruments': instruments}
            print(url)
            req = requests.Request(
                'GET', url, headers=self.headers)
            pre = req.prepare()
            resp = s.send(pre, verify=True)
            return resp
        except Exception as e:
            s.close()
            print("Caught exception when connecting to stream\n" + str(e))

    def get_all_instruments(self):

        # URL to receive all currency pairs listed on API
        url = "https://api-fxpractice.oanda.com/v3/accounts/{}/instruments".format(
            account_id)
        instruments = self.send_request(
            url, ArbitrageWrapper.headers)['instruments']
        instrument_names = []

        # Loop to add instrument data to pair_data object
        for instrument in instruments:
            name = instrument["name"]
            instrument_names.append(name)

        return instrument_names

    def get_instrument_rates(self, instrument):
        bid_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=1&price=B&granularity=S5".format(
            instrument)
        ask_url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles?count=1&price=A&granularity=S5".format(
            instrument)
        bid = float(self.send_request(bid_url, ArbitrageWrapper.headers)[
                    'candles'][0]['bid']['c'])
        ask = float(self.send_request(ask_url, ArbitrageWrapper.headers)[
                    'candles'][0]['ask']['c'])
        rates = {
            "name": instrument,
            "bid": bid,
            "ask": ask
        }
        return rates

    def make_instrument_triangles(self, instruments):

        # Making a list of all instrument pairs (based on quoted currency)
        first_instruments = []
        for instrument in itertools.combinations(instruments, 2):
            quote1 = instrument[0][4:]
            if quote1 in instrument[1]:
                first_instruments.append((instrument[0], instrument[1]))

        # Adding the final instrument to the pairs to convert currency back to starting (based on the currency only in one pair and the starting currency)
        for instrument in first_instruments:
            currency1 = instrument[0][:3]
            currency2 = instrument[0][4:]
            currency3 = instrument[1][:3]
            currency4 = instrument[1][4:]
            currencies = [currency1, currency2]
            if currency3 not in currencies:
                currencies.append(currency3)
            elif currency4 not in currencies:
                currencies.append(currency4)
            for combo in itertools.combinations(currencies, 2):
                combo_str = combo[0] + '_' + combo[1]
                if combo_str not in instrument and combo_str in instruments:
                    instruments.append(
                        (instrument[0], instrument[1], combo_str))

        return instruments

    def make_tri_w_starting_curr(self, triangles):
        tri_w_starting_curr = []
        for pair in triangles:
            for instrument in pair:
                if self.starting_currency in instrument and pair not in tri_w_starting_curr:
                    tri_w_starting_curr.append(pair)
        return tri_w_starting_curr

    def connect_to_stream(self, instruments):
        """
        Environment                 Description 
        fxTrade (Live)              The live (real money) environment 
        fxTrade Practice (Demo)     The demo (simulated money) environment 
        """
        domainDict = {'live': 'stream-fxtrade.oanda.com',
                      'demo': 'stream-fxpractice.oanda.com'}
        domain = domainDict[ArbitrageWrapper.environment]
        try:
            s = requests.Session()
            url = "https://" + domain + \
                "/v3/accounts/{}/pricing/stream?instruments={}".format(
                    account_id, instruments)
            # params = {'instruments': instruments}
            print(url)
            req = requests.Request(
                'GET', url, headers=self.headers)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=True)
            return resp
        except Exception as e:
            s.close()
            print("Caught exception when connecting to stream\n" + str(e))

    def arb_calculator(self, obj):
        edge_pair = []
        mid_pair = ''

        # Get possible starting pairs based on starting_currency
        for key, value in obj.items():
            if self.starting_currency in key:
                edge_pair.append(key)
            else:
                mid_pair = key
        pairing_1 = (edge_pair[0], mid_pair, edge_pair[1])
        pairing_2 = (edge_pair[1], mid_pair, edge_pair[0])
        pairing_orders = [pairing_1, pairing_2]

        # To run both pairing order options
        for pairing in pairing_orders:
            balance = self.starting_balance
            currency = self.starting_currency
            total_commission = 0
            trades = []

            for x in range(0, len(pairing)):
                base = pairing[x][:3]
                quote = pairing[x][4:]

                if base == currency:
                    # We are buying base/quote at the ask price
                    price = obj[pairing[x]]['ask']
                    units = balance / price
                    balance = balance * (1 * price)
                    currency = quote
                    trade_commission = ((units / 100000) * 5.00)
                    total_commission += trade_commission
                    trade = {
                        'instrument': pairing[x],
                        'order_type': 'BUY',
                        'units': units,
                        'bid/ask': 'ASK',
                        'price': price,
                        'new_balance': balance,
                        'new_currency': currency,
                        'trade_commission': trade_commission
                    }
                    trades.append(trade)

                elif quote == currency:
                    # We are selling base/quote at the bid price
                    price = obj[pairing[x]]['bid']
                    units = balance / price
                    balance = balance * (1 / price)
                    currency = base
                    trade_commission = ((units / 100000) * 5.00)
                    total_commission += trade_commission
                    trade = {
                        'instrument': pairing[x],
                        'order_type': 'SELL',
                        'units': -units,
                        'bid/ask': 'BID',
                        'price': price,
                        'new_balance': balance,
                        'new_currency': currency,
                        'trade_commission': trade_commission
                    }
                    trades.append(trade)

            profit = balance - self.starting_balance
            net_profit = profit - total_commission

            if net_profit > 0:
                result = {
                    'trades': trades,
                    'balance': balance,
                    'currency': currency,
                    'profit': profit,
                    'total_commission': total_commission,
                    'net_profit': net_profit
                }
                return result

    def place_limit_order(self, trade):
        domainDict = {'live': 'stream-fxtrade.oanda.com',
                      'demo': 'stream-fxpractice.oanda.com'}
        domain = domainDict[ArbitrageWrapper.environment]
        pprint.pprint(trade)
        try:
            data = {
                "order": {
                    "price": str(trade['price']),
                    # "stopLossOnFill": {
                    #   "timeInForce": "GTC",
                    #   "price": "1.7000"
                    # },
                    # "takeProfitOnFill": {
                    #   "price": "1.14530"
                    # },
                    "timeInForce": "GTC",
                    "instrument": str(trade['instrument']),
                    "units": str(round(trade['units'], 0)),
                    "type": "LIMIT",
                    "positionFill": "DEFAULT"
                }
            }
            # data = {
            #   "order": {
            #     "units": str(round(trade['units'], 0)),
            #     "instrument": str(trade['instrument']),
            #     "timeInForce": "FOK",
            #     "type": "MARKET",
            #     "positionFill": "DEFAULT"
            #   }
            # }
            pprint.pprint(data)

            # s = requests.Session()
            url = "https://api-fxpractice.oanda.com/v3/accounts/{}/orders".format(
                account_id)
            r = requests.post(url, headers=ArbitrageWrapper.headers, json=data)
            return r

        except Exception as e:
            # s.close()
            print("Caught exception when connecting to stream\n" + str(e))
