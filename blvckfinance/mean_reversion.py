import requests 
import pandas as pd 
import numpy as np 

import os
api_key = os.getenv('api_key')


stock = 'AAPL'
stockprices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}').json()

stockprices = stockprices['historical'][0:1200]

stockprices = pd.DataFrame.from_dict(stockprices)
stockprices = stockprices.set_index('date')

stockprices = stockprices.iloc[::-1]

stockprices['20d'] = stockprices['close'].rolling(20).mean() 


stockprices['return'] = np.log(stockprices['close'] / stockprices['close'].shift(1) )


stockprices['difference'] = stockprices['close'] - stockprices['20d']

stockprices['long'] = np.where(stockprices['difference'] < -2 ,1,np.nan)
stockprices['long'] = np.where(stockprices['difference'] * stockprices['difference'].shift(1) < 0, 0, stockprices['long'])
stockprices['long'] = stockprices['long'].ffill().fillna(0)

stockprices['gain_loss'] = stockprices['long'].shift(1) * stockprices['return']
stockprices = stockprices.dropna(subset=['20d'])

stockprices['total'] =  stockprices['gain_loss'].cumsum()
print(stockprices.tail(30))