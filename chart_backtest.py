# Testing w/ Oanda REST-V20 API
from config import key, account_id
import requests
import json
import pprint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# URL for instrument candle data
eur_usd_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5"

# Headers required for API access
headers = {
    "Authorization": key
}

# Function to receive API data
def send_request(url, headers):
    r = requests.get(url, headers=headers).json()
    return r

# Matplot 
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Used to increment candle in candles 
candle_no = 0
candles = send_request(eur_usd_url, headers)

# Empty lists to capture time (x) and currency pair price (y) as it is refreshed 
xs = []
ys = []

# Function to fetch and plot data as it is refreshed 
def animate(i):
    global candle_no
    
    if candle_no < 6:
      time = candles['candles'][candle_no]['time'][11:19]
      close = candles['candles'][candle_no]['mid']['c']

      xs.append(time)
      ys.append(close)

      ax1.clear()
      ax1.plot(xs, ys)

      candle_no += 1
    else: 
      print('No more candles to print')

# Running the actual function every second
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()