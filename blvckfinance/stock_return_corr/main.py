import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf
from statsmodels import api as sm
from scipy.stats import linregress


stocks =['AAPL','MSFT','FB','GME','TSLA','AMZN']
stock_list = []
for stock in stocks:
  returns = yf.Ticker(stock)
  returns = returns.history(period="1y")
  returns['returns'] =  returns['Close'].pct_change()

  returns.rename(columns={'returns': stock}, inplace=True)
  returns = returns[stock]
  stock_list.append(returns)

all_stock_returns =pd.DataFrame(stock_list).T

#statistics
all_stock_returns.describe()
#calculate correlation
correlation = all_stock_returns.corr()
sm.graphics.plot_corr(correlation,xnames=list(correlation.columns))

all_stock_returns = all_stock_returns.iloc[1:]
print(linregress(all_stock_returns['AAPL'],all_stock_returns['MSFT']))
print(linregress(all_stock_returns['AAPL'],all_stock_returns['GME']))