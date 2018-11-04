import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

x_profit = []
y_profit = []
x_loss = []
y_loss = []

graph_data = open('example.txt','r').read()
lines = graph_data.split('\n')
for line in lines:
  if len(line) > 1:
    x, y = line.split(',')
    print(x,y)
    if float(y) > 0:
      x_profit.append(float(x))
      y_profit.append(float(y))
    elif float(y) <= 0:
      x_loss.append(float(x))
      y_loss.append(float(y))

plt.scatter(x_profit, y_profit, label='Profitable Currency Pairing', color='k', s=25, marker="*")
plt.scatter(x_loss, y_loss, label='Negative Currency Pairing', color='k', s=25, marker=".")

plt.xlabel('Currency Pairing #')
plt.ylabel('Profit Margin')
plt.title('Forex Arbitrage')
plt.legend()
plt.show()