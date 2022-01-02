import requests
from datetime import datetime
from time import time 
import pandas as pd 
import matplotlib.pyplot as plt 

base_url = "https://api.kucoin.com"
coin_pair = "BTC-USDT" #BTC-USDT 
frequency = "4hour" #1hour 4hour 1min
#get timestamp date of today in seconds
now_is = int(time())
days = 400
            #sec  min  hour days
days_delta = 60 * 60 * 24 * days 
start_At = now_is - days_delta
#print(now_is)
price_url = f"/api/v1/market/candles?type={frequency}&symbol={coin_pair}&startAt={start_At}&endAt={now_is}"


price_dict = {}

prices = requests.get(base_url+price_url).json()
for item in prices['data']:
  #convert date from timestamp to Y M D
  date_converted = datetime.fromtimestamp(int(item[0])).strftime("%Y-%m-%d")
  price_dict[date_converted] = item[2]
price_dict
priceDF = pd.DataFrame(price_dict,index=["price"]).T
priceDF['price'] = priceDF['price'].astype(float)

#convert dates to datetime from object
priceDF.index = pd.to_datetime(priceDF.index)

#reverse dates
priceDF = priceDF.iloc[::-1]

#moving_average 200 days(
priceDF['200MA'] = priceDF['price'].rolling(200).mean()
priceDF['52MA'] = priceDF['price'].rolling(52).mean()

priceDF

#plot 

fig, ax = plt.subplots()
ax.plot(priceDF[['price','200MA','52MA']])
# Rotate and align the tick labels so they look better.
fig.autofmt_xdate()
ax.legend(['price','200MA','52MA'])
# Use a more precise date string for the x axis locations in the toolbar.

plt.show()