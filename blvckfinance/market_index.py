import requests
import os
api_key = os.getenv('api_key')
your_api_key = api_key

#get quote data from API
AAPL = requests.get(f'https://financialmodelingprep.com/api/v3/quote/AAPL?apikey={your_api_key}').json()
MSFT = requests.get(f'https://financialmodelingprep.com/api/v3/quote/MSFT?apikey={your_api_key}').json()
GOOG = requests.get(f'https://financialmodelingprep.com/api/v3/quote/GOOG?apikey={your_api_key}').json()

#Parse PRice 
AAPL_price = AAPL[0]['price']
MSFT_price = MSFT[0]['price']
GOOG_price = GOOG[0]['price']

#calculate Weights
Weight_AAPL = AAPL_price / (AAPL_price+MSFT_price+GOOG_price)
Weight_MSFT = MSFT_price / (AAPL_price+MSFT_price+GOOG_price)
Weight_GOOG = GOOG_price / (AAPL_price+MSFT_price+GOOG_price)

print('Apple Weight is: ' + str(Weight_AAPL) + '  Microsoft Weight is: ' + str(Weight_MSFT) + '  Google Weight is: ' + str(Weight_GOOG)  )