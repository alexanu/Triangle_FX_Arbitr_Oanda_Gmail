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

    def __init__(self, starting_balance, starting_currency):
        print('Attempting to find arbitrage')
        print('Balance: ' + str(starting_balance) + ' ' + starting_currency)

    def send_request(self, url, headers):
        r = requests.get(url, headers=headers).json()
        return r

    def get_all_instruments(self):

        # URL to receive all currency pairs listed on API
        url = "https://api-fxpractice.oanda.com/v3/accounts/101-001-9183876-001/instruments"
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

    def make_instrument_combos(self, instruments):

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
                    instruments.append((instrument[0], instrument[1], combo_str))

        return instruments

    def arb_calculator(self, obj, starting_balance, starting_currency):
        edge_pair = []
        mid_pair = ''

        # Get possible starting pairs based on starting_currency
        for key, value in obj.items():
            if starting_currency in key:
                edge_pair.append(key)
            else:
                mid_pair = key
        pairing_1 = (edge_pair[0], mid_pair, edge_pair[1])
        pairing_2 = (edge_pair[1], mid_pair, edge_pair[0])
        pairing_orders = [pairing_1, pairing_2]

        # To run both pairing order options
        for pairing in pairing_orders:
            balance = starting_balance
            currency = starting_currency
            for x in range(0, len(pairing)):
                base = pairing[x][:3]
                quote = pairing[x][4:]

                if base == currency:
                    # We are buying base/quote at the ask price
                    balance = balance * (1 * obj[pairing[x]]['ask'])
                    currency = quote

                elif quote == currency:
                    # We are selling base/quote at the bid price
                    balance = balance * (1 / obj[pairing[x]]['bid'])
                    currency = base

            profit = round(balance - starting_balance, 5)
            profit_margin = round((profit / balance) * 100, 5)
            
            if profit > 0:
                print('Arbitrage Detected')
                print('Trade in this order: {} for a profit of ${} {} ({} %)'.format(
                    pairing, profit, currency, profit_margin))
                print(
                    '-------------------------------------------------------------------------------------------')

                result_object = {
                    "steps": pairing,
                    "profit": profit,
                    "profit_margin": profit_margin,
                    "currency": currency
                }
                return result_object