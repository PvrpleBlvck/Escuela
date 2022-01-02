import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
api_key = os.getenv('api_key')
#Variables
stocks = ['NVS','AAPL','MSFT','GOOG']
#initial_weight = np.array([0.20,0.30,0.30,0.20])

RF = 0

empresas = {}
#api_key = 'your api key'
#Get all prices into a dataframe
for stock in stocks:
  prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}').json()

  prices = prices['historical'][-900:]

  prices = pd.DataFrame(prices) 
  
  empresas[stock] = prices.set_index('date')
  empresas[stock] = empresas[stock]['close']

portfolio = pd.concat(empresas, axis=1)
return_stocks = portfolio.pct_change()

number_of_portfolios = 2000
RF = 0


portfolio_returns = []
portfolio_risk = []
sharpe_ratio_port = []
portfolio_weights = []

for portfolio in range (number_of_portfolios):
  #generate a w random weight of lengt of number of stocks
  weights = np.random.random_sample((len(stocks)))
 
  weights = weights / np.sum(weights)
  annualize_return = np.sum((return_stocks.mean() * weights) * 252)
  portfolio_returns.append(annualize_return)
  #variance
  matrix_covariance_portfolio = (return_stocks.cov())*252
  portfolio_variance = np.dot(weights.T,np.dot(matrix_covariance_portfolio, weights))
  portfolio_standard_deviation= np.sqrt(portfolio_variance) 
  portfolio_risk.append(portfolio_standard_deviation)
  #sharpe_ratio
  sharpe_ratio = ((annualize_return- RF)/portfolio_standard_deviation)
  sharpe_ratio_port.append(sharpe_ratio)

  portfolio_weights.append(weights)

portfolio_risk = np.array(portfolio_risk)
portfolio_returns = np.array(portfolio_returns)
sharpe_ratio_port = np.array(sharpe_ratio_port)

plt.figure(figsize=(10, 5))
plt.scatter(portfolio_risk, portfolio_returns, c=portfolio_returns / portfolio_risk) 
plt.xlabel('volatility')
plt.ylabel('returns')
plt.colorbar(label='Sharpe ratio')

porfolio_metrics = [portfolio_returns,portfolio_risk,sharpe_ratio_port, portfolio_weights] 

portfolio_dfs = pd.DataFrame(porfolio_metrics)
portfolio_dfs = portfolio_dfs.T
portfolio_dfs.columns = ['Port Returns','Port Risk','Sharpe Ratio','Portfolio Weights']

#convert from object to float the first three columns.
for col in ['Port Returns', 'Port Risk', 'Sharpe Ratio']:
    portfolio_dfs[col] = portfolio_dfs[col].astype(float)

#portfolio with the highest Sharpe Ratio
Highest_sharpe_port = portfolio_dfs.iloc[portfolio_dfs['Sharpe Ratio'].idxmax()]
#portfolio with the minimum risk 
min_risk = portfolio_dfs.iloc[portfolio_dfs['Port Risk'].idxmin()]

#Highest_sharpe_port
print(Highest_sharpe_port)
print(min_risk)