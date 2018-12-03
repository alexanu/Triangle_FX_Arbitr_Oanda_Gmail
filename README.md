# Algo Trading Bots
- Created from scratch by Troy Smith

![Quantitative Finance](https://miro.medium.com/max/884/1*SfUnSwcp9mVJB4EH2lPtOQ.png)






## What is 'Algorithmic Trading'?
Algorithmic trading is a type of trading done with the use of mathematical formulas run by powerful computers. An algorithm, in mathematics, is a set of directions for solving a problem. An example of an algorithm is an algebraic equation, combined with the formal rules of algebra. With the these two elements, a computer could derive the answer to that equation every time.

Algorithmic trading makes use of much more complex formulas, combined with mathematical models and human oversight, to make decisions to buy or sell financial securities on an exchange. Algorithmic traders often make use of high-frequency trading technology, which can enable a firm to make tens of thousands of trades per second.

[Investopedia](https://www.investopedia.com/terms/a/algorithmictrading.asp#ixzz5WlaWZKNw)






## My Strategies

### SMA5 Mean Reversion
This is a basic algo trading strategy, which operates under the assumption that markets are ranging 80% of the time. Black boxes that employ this strategy typically calculate an average asset price using historical data and takes trades in anticipation of the current price returning to the average price. 

Steps:
- Look at the 5-day moving average and trade from the other side
- Long if current price is below its moving average and Short if it is above
- Check that instruments bid/ask price every time there is a price chang(Stream API)
- Sell/Buy back when price crosses 5-day SMA


### Simple Short
This strategy was created for learning purposes only. It is basically just my own implementation of a continuous random instrument short w/ a take profit. 

Steps:
- Ask the user what instrument they want to short and how many units
- Short that instrument for that many units
- Check that instruments ask price every time the price changes (Stream API)
- Buy back instrument for same amount of units when profit reaches predetermined threshold


### Arbitrage (Triangular)
I created this trading bot to exploit and take advantage of pricing inefficiencies in the foreign exchange market. The strategy implemented is risk-free and will allow the user to make a profit with no open currency exposure.






## Other Strategies 

### Trend-following

One of the simplest strategies is simply to follow market trends, with buy or sell orders generated based on a set of conditions fulfilled by technical indicators. This strategy can also compare historical and current data in predicting whether trends are likely to continue or reverse.

### Mean reversion

Another basic kind of algo trading strategy is the mean reversion system, which operates under the assumption that markets are ranging 80% of the time. Black boxes that employ this strategy typically calculate an average asset price using historical data and takes trades in anticipation of the current price returning to the average price.

### News-based

Ever try trading the news? Well, this strategy can do it for you! A news-based algorithmic trading system is usually hooked to news wires, automatically generating trade signals depending on how actual data turns out in comparison to the market consensus or the previous data.

### Market sentiment

As you’ve learned in our School lesson on market sentiment, commercial and non-commercial positioning can also be used to pinpoint market tops and bottoms. Forex algo strategies based on market sentiment can involve using the COT report or a system that detects extreme net short or long positions. More modern approaches are also capable of scanning social media networks to gauge currency biases.

### Arbitrage

Now here’s where it gets a little more complicated than usual. Making use of arbitrage in algorithmic trading means that the system hunts for price imbalances across different markets and makes profits off those. Since the forex price differences are in usually micropips though, you’d need to trade really large positions to make considerable profits. Triangular arbitrage, which involves two currency pairs and a currency cross between the two, is also a popular strategy under this classification.

### High-frequency trading

As the name suggests, this kind of trading system operates at lightning-fast speeds, executing buy or sell signals and closing trades in a matter of milliseconds. These typically use arbitrage or scalping strategies based on quick price fluctuations and involves high trading volumes.

### “Iceberging”

This is a strategy employed by large financial institutions who are very secretive about their forex positions. Instead of placing one huge long or short position with just one broker, they break up their trade into smaller positions and execute these under different brokers. Their algorithm can even enable these smaller trade orders to be placed at different times to keep other market participants from finding out! This way, financial institutions are able to execute trades under normal market conditions without sudden price fluctuations. Retail traders who keep track of trading volumes are able to see only the “tip of the iceberg” when it comes to these large trades.

### Stealth

If you think iceberging is sneaky, then the stealth strategy is even sneakier! Iceberging has been such a common practice in the past few years that hardcore market watchers were able to hack into this idea and come up with an algorithm to piece together these smaller orders and figure out if a large market player is behind all of it.



## Technical Indicators

### RSI

### MACD

### Candlestick Patterns



## Learning Resources
For anyone interested in learning algorithmic trading, I suggest starting out on one of the following web services:
- Quantopian
- QuantConnect
- QuantRocket