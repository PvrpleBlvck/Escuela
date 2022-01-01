import requests
import pandas as pd
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

import os
api_key = os.getenv('api_key')

def historical_prices(stock):
	historical_prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?apikey={api_key}').json()

	historical_prices = historical_prices['historical']
	price_data = {}

	for item in historical_prices:
		price_data[item['date']] = {}
		price_data[item['date']]['date'] = item['date']
		price_data[item['date']]['open']= item['open']
		price_data[item['date']]['high'] = item['high']
		price_data[item['date']]['low'] = item['low']
		price_data[item['date']]['adjClose'] = item['adjClose']

	price_DF = pd.DataFrame.from_dict(price_data)
	price_DF = price_DF.T	
	fig = go.Figure(data=[go.Candlestick(x=price_DF['date'],
                open=price_DF['open'],
                high=price_DF['high'],
                low=price_DF['low'],
                close=price_DF['adjClose'])])

	fig.show()

def income_statement(stock):
 	number_qts = input('number_qts').strip()
 	IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit={number_qts}&apikey={api_key}').json()
 	IS = pd.DataFrame.from_dict(IS)
 	print(IS.T)
 	save_to_csv = input('save_to_csv? y or n').strip()
 	if save_to_csv == 'y':
 		IS.to_csv('IS.csv')

def profile(stock):
	profile = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_key}').json()
	profile = profile[0]
	print(profile)
	
def balance_sheet(stock):
	number_qts = input('number_qts?').strip()
	save_to_csv = input('save_to_csv? y or n').strip()
	BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&limit={number_qts}&apikey={api_key}').json()
	BS = pd.DataFrame.from_dict(BS)
	BS = BS.T
	if save_to_csv == 'y':
		BS.to_csv('BS.csv')

	print(BS)

def valuation_dcf(stock):
	valuation_dcf = requests.get(f'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{stock}?apikey={api_key}').json()
	DCF= valuation_dcf[0]['dcf']
	stock_price = valuation_dcf[0]['Stock Price']
	print('Current Stock Price is ' + str(stock_price) + '. Price as per DCF valuation is ',str(DCF))

def dividends(stock):
	number_of_dividends = input('number_qts?').strip()
	number_of_dividends = int(number_of_dividends)
	dividends = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{stock}?apikey={api_key}').json()
	dividends = dividends['historical'][0:number_of_dividends]

	for item in dividends:
		print(item['paymentDate'] + ' :' + ' Dividend was :' + str(item['dividend']))


while True:
    comman = input('stock?')
    command = comman.split(' ')[0] + ' '
    stock = comman.split(' ')[1]
    if comman == 'IS ' + stock :
        income_statement(stock)
    elif comman == 'profile ' + stock:
        profile(stock)
    elif comman == 'BS ' + stock:
    	balance_sheet(stock)
    elif comman == 'dividends ' + stock:
    	dividends(stock)
    elif comman == 'DCF ' + stock:
    	valuation_dcf(stock)
    elif comman == 'quit':
        break
    elif comman == 'prices ' + stock:
        historical_prices(stock)
    else:
        print('Invalid Command.')