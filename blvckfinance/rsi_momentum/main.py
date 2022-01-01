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

#reverse dates in the index to have more recent days at the end
stockprices = stockprices.iloc[::-1]

#calculate the return of the day and add as new column
stockprices['return'] = np.log(stockprices['close'] / stockprices['close'].shift(1) )

#calculate the movement on the price compared to the previous day closing price
stockprices['movement'] = stockprices['close'] - stockprices['close'].shift(1)

stockprices['up'] = np.where((stockprices['movement'] > 0) ,stockprices['movement'],0)

stockprices['down'] = np.where((stockprices['movement'] < 0) ,stockprices['movement'],0)

window_length = 14
#calculate moving average of the last 14 days  gains
up = stockprices['up'].rolling(window_length).mean()

#calculate moving average of the last 14 days  losses
down = stockprices['down'].abs().rolling(window_length).mean()

RS = up / down

RSI = 100.0 - (100.0 / (1.0 + RS))

RSI = RSI.rename("RSI")
print(RSI)


ew = pd.merge(stockprices, RSI, left_index=True, right_index=True)

#If the indicator’s line crosses the level 30 from below, a long position (Buy) is opened.  
new['long'] = np.where((new['RSI'] < 30),1,np.nan)
new['long'] = np.where((new['RSI'] > 70),0,new['long'])

new['long'].ffill(inplace=True)

new['gain_loss'] = new['long'].shift(1) * new['return']

new['total'] =  new['gain_loss'].cumsum()

print(new.tail(600))

alternative strategy of buying and hold stock:
return_holding = (new['close'][-1] - new['close'][1]) / new['close'][1]
print(return_holding)