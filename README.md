# Forex Trading Bots
Developed from scratch by Troy Smith

![Quantitative Finance](https://miro.medium.com/max/884/1*SfUnSwcp9mVJB4EH2lPtOQ.png)


## What is 'Algorithmic Trading'
Algorithmic trading is a type of trading done with the use of mathematical formulas run by powerful computers. An algorithm, in mathematics, is a set of directions for solving a problem. An example of an algorithm is an algebraic equation, combined with the formal rules of algebra. With the these two elements, a computer could derive the answer to that equation every time.

Algorithmic trading makes use of much more complex formulas, combined with mathematical models and human oversight, to make decisions to buy or sell financial securities on an exchange. Algorithmic traders often make use of high-frequency trading technology, which can enable a firm to make tens of thousands of trades per second.

[Investopedia](https://www.investopedia.com/terms/a/algorithmictrading.asp#ixzz5WlaWZKNw)


## My Strategies

### Simple Short
This strategy was created for learning purposes only. It is basically just my own implementation of a take profit. 

#### Steps:
- Ask the user what instrument they want to short and how many units
- Short that instrument for that many units
- Check that instruments ask price every time the price changes (Stream API)
- Buy back instrument for same amount of units when profit reaches predetermined threshold

### Triangular Arbitrage
I created this trading bot to exploit and take advantage of pricing inefficiencies in the foreign exchange market. The strategy implemented is risk-free and will allow the user to make a profit with no open currency exposure.


## Learning
For anyone interested in learning algo trading, I suggest starting out on one of the following web services
- Quantopian
- QuantConnect
- QuantRocket