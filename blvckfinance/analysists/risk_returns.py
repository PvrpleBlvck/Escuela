import requests
import pandas as pd
import numpy as np

#Variables
stocks = ['NVS','AAPL','MSFT','GOOG']
initial_weight = np.array([0.20,0.30,0.30,0.20])
empresas = {}

#Get all prices into a dataframe
for stock in stocks:
  prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line').json()

  prices = prices['historical'][-900:]

  prices = pd.DataFrame(prices) 
  
  empresas[stock] = prices.set_index('date')
  empresas[stock] = empresas[stock]['close']

#Concatenate each of the dataframes into a single dataframe
portfolio = pd.concat(empresas, axis=1)

return_stocks = portfolio.pct_change()
return_stocks.head(10)

daily_returns_portfolio_mean = return_stocks.mean()
print(daily_returns_portfolio_mean)

allocated_daily_returns = (initial_weight * daily_returns_portfolio_mean)

portfolio_return = np.sum(allocated_daily_returns)
print(portfolio_return)

# calculate portfolio daily returns
return_stocks['portfolio_daily_returns'] = return_stocks.dot(initial_weight)
return_stocks

Cumulative_returns_daily = (1+return_stocks).cumprod()
Cumulative_returns_daily.tail(5)

Cumulative_returns_daily['portfolio_daily_returns'].plot()

matrix_covariance_portfolio = return_stocks.iloc[:,:-1]
matrix_covariance_portfolio = (matrix_covariance_portfolio.cov())*252

matrix_covariance_portfolio


portfolio_variance = np.dot(initial_weight.T,np.dot(matrix_covariance_portfolio, initial_weight))

#standard deviation (risk of portfolio)
portfolio_risk = np.sqrt(portfolio_variance)
portfolio_risk
