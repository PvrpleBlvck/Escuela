#List of symbols https://financialmodelingprep.com/api/v3/quotes/forex

import requests
import pandas as pd
import matplotlib.pyplot as plt

exchange_rates_Python = {}
currencies = ['EURUSD','CHFUSD=X','AUDUSD','GBPUSD']

for currency in currencies:
  forex = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/forex/{currency}')

  forex = forex.json()
  exchange_rates_Python[currency] = {}

  for item in forex['historical']:
    adj_close = item['adjClose']
    trade_date = item['date']
    exchange_rates_Python[currency][trade_date] = adj_close


currencies_df = pd.DataFrame.from_dict(exchange_rates_Python, orient='index')
currencies_df=currencies_df.T
currencies_df.index = pd.to_datetime(currencies_df.index)


#take last 30 days
currencies_df = currencies_df.iloc[:90,:]

fig, axes = plt.subplots(nrows=2, ncols=2)

currencies_df[currencies[0]].plot(ax=axes[0,0])
axes[0,0].set_title(currencies[0])

currencies_df[currencies[1]].plot(ax=axes[0,1])
axes[0,1].set_title(currencies[1])

currencies_df[currencies[2]].plot(ax=axes[1,0])
axes[1,0].set_title(currencies[2])

currencies_df[currencies[3]].plot(ax=axes[1,1])
axes[1,1].set_title(currencies[3])

plt.tight_layout()
plt.show()