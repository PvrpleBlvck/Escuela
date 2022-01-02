import requests
import pandas as pd 
import time
import os
api_key = os.getenv('api_key')

def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]

	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

companies = get_sp500()
companies.insert(0,'^GSPC')


print(companies)
#api_key = 'your api key'
price = {}
metrics = {}
count = 0
for company in companies:
	count = count + 1
	time.sleep(3)
	print('count ' ,count)
	try:
		prices_retrieval = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries=500&apikey={api_key}').json()
		prices_retrieval = prices_retrieval['historical']
		price[company] = {}
		metrics[company] = {}
		for item in prices_retrieval:
			price_date = item['date']
			price[company][price_date] = item['adjClose']
			
		price_DF = pd.DataFrame.from_dict(price)
		price_DF['200_MA'] = price_DF[company].rolling(window=200).mean()
		price_DF['150_MA'] = price_DF[company].rolling(window=150).mean()
		price_DF['50_MA'] = price_DF[company].rolling(window=50).mean()
		price_DF['RS'] = (price_DF[company][–1]/price_DF['^GSPC'][–1] )/ (price_DF[company][–252]/price_DF['^GSPC'][–252]) *100
	
		metrics[company]['200 MA'] = price_DF['200_MA'][–1]
		metrics[company]['150 MA'] = price_DF['150_MA'][–1]
		metrics[company]['50 MA'] = price_DF['50_MA'][–1]
		metrics[company]['200 MA_1mago'] = price_DF['200_MA'][–30]
		metrics[company]['150 MA_1mago'] = price_DF['150_MA'][–30]
		metrics[company]['200 MA_2mago'] = price_DF['200_MA'][–60]
		metrics[company]['150 MA_2mago'] = price_DF['150_MA'][–60]
		metrics[company]['52W_Low'] = price_DF[company][–252:].min()
		metrics[company]['52W_High'] = price_DF[company][–252:].max()
		metrics[company]['price'] = price_DF[company][–1]
		metrics[company]['Relative Strength'] = price_DF['RS'][–1]
		#Current Price is at least 30% above 52 week low (1.3*low_of_52week)
		metrics[company]['Above_30%_low'] = metrics[company]['52W_Low'] *1.3
		# Condition 7: Current Price is within 25% of 52 week high   (.75*high_of_52week)
		metrics[company]['Within_25%_high'] = metrics[company]['52W_High'] * 0.75
	except:
		pass
		


metrics_DF = pd.DataFrame.from_dict(metrics)
metrics_DF = metrics_DF.T 
#to determine the rank percentil and see which are the 80% top performers
metrics_DF['pct_rank'] = metrics_DF['Relative Strength'].rank(pct=True)
metrics_DF = metrics_DF.T
metrics_DF.to_csv('all_stocks_SP500.csv')
print(metrics_DF)


