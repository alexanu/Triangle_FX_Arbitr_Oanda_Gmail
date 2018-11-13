from collections import defaultdict
from operator import itemgetter
from time import time
from config import *
import requests

FEE = 0.0000
PRIMARY = ['USD', 'EUR', 'GBB']
headers = {
    # "Content-Type": "application/json",
    "Authorization": key
}

def main():
    print('main')
    start_time = time()

    prices = get_prices()
    prices_time = time()
    print(f"Downloaded in: {prices_time - start_time:.4f}s")
    print(prices)
    
    # triangles = list(find_triangles(prices))
    # print(f"Computed in: {time() - prices_time:.4f}s")

    # if triangles:
    #     for triangle in sorted(triangles, key=itemgetter('profit'), reverse=True):
    #         describe_triangle(prices, triangle)
    # else:
    #     print("No triangles found, try again!")

def get_rate(instrument):
  bid_url = "https://api-fxpractice.oanda.com/v3/accounts/{}/pricing?instruments={}".format(account_id, instrument)
  ask_url = "https://api-fxpractice.oanda.com/v3/accounts/{}/pricing?instruments={}".format(account_id, instrument)
  bid = requests.get(bid_url, headers).json()
  ask = requests.get(ask_url, headers).json()
  print(bid)
  
  # ticker = {
  #   'symbol': instrument,
  #   'bidPrice': float(bid['candles'][0]['bid']['c']),
  #   'askPrice': float(ask['candles'][0]['ask']['c'])
  # }
  # prices = [ticker]
  # return prices

def get_prices():
    prices = get_rate('EUR_USD')

    # client = Client(None, None)
    # prices = client.get_orderbook_tickers()
    prepared = defaultdict(dict)
    for ticker in prices:
        pair = ticker['symbol']
        ask = float(ticker['askPrice'])
        bid = float(ticker['bidPrice'])
        for primary in PRIMARY:
            if pair.endswith(primary):
                secondary = pair[:-len(primary)]
                prepared[primary][secondary] = 1 / ask
                prepared[secondary][primary] = bid
    return prepared


def find_triangles(prices):
    pass
    # triangles = []
    # starting_coin = 'BTC'
    # for triangle in recurse_triangle(prices, starting_coin, starting_coin):
    #     coins = set(triangle['coins'])
    #     if not any(prev_triangle == coins for prev_triangle in triangles):
    #         yield triangle
    #         triangles.append(coins)


def recurse_triangle(prices, current_coin, starting_coin, depth_left=3, amount=1.0):
    pass
    # if depth_left > 0:
    #     pairs = prices[current_coin]
    #     for coin, price in pairs.items():
    #         new_price = (amount * price) * (1.0 - FEE)
    #         for triangle in recurse_triangle(prices, coin, starting_coin, depth_left - 1, new_price):
    #             triangle['coins'] = triangle['coins'] + [current_coin]
    #             yield triangle
    # elif current_coin == starting_coin and amount > 1.0:
    #     yield {
    #         'coins': [current_coin],
    #         'profit': amount
    #     }


def describe_triangle(prices, triangle):
    pass
    # coins = triangle['coins']
    # price_percentage = (triangle['profit'] - 1.0) * 100
    # print(f"{'->'.join(coins):26} {round(price_percentage, 4):-7}% <- profit!")
    # for i in range(len(coins) - 1):
    #     first = coins[i]
    #     second = coins[i + 1]
    #     print(f"     {second:4} / {first:4}: {prices[first][second]:-17.8f}")
    # print('')


if __name__ == '__main__':
    main()