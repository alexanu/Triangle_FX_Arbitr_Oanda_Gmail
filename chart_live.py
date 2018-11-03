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

# Helper function to fetch candle data
def send_request(url, headers):
    r = requests.get(url, headers=headers).json()
    # pprint.pprint(r)
    return r

# Matplot
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Empty lists to capture time (x) and currency pair price (y) as it is refreshed
xs = []
ys = []

# Function to fetch and plot data as it is refreshed
def animate(i):
    candle = send_request(eur_usd_url, headers)['candles'][0]

    time = candle['time'][11:19]
    close = float(candle['mid']['c'])

    xs.append(time)
    ys.append(close)

    ax1.clear()
    ax1.plot(xs, ys)


# Running the actual function every second
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()