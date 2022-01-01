import requests 
import pandas as pd

import requests
import os
api_key = os.getenv('fmpapi_key')

demo= api key

companies = requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector=technology&marketCapMoreThan=100000000000&limit=100&apikey={demo}')
companies = companies.json()

technological_companies = []

for item in companies:
  technological_companies.append(item['symbol'])
print(technological_companies)
# outcome
['MSF.BR',
 'MSFT',
 'AAPL',
 'AMZN',
 'GOOG',....



 metrics = {}
for item in technological_companies:
    try:
      metrics[item] = {}
      keymetrics = requests.get(f'https://fmpcloud.io/api/v3/ratios/{item}?apikey={demo}')
      keymetrics = keymetrics.json()
      keymetrics[0]

      metrics[item]['date'] = keymetrics[0]['date']
      metrics[item]['currentratio'] = float(keymetrics[0]['currentRatio'])

      metrics[item]['debtToAssets'] = float(keymetrics[0]['debtRatio'])
      metrics[item]['debtToEquity'] = float(keymetrics[0]['debtEquityRatio'])
      metrics[item]['dividendYield'] = float(keymetrics[0]['dividendYield'])

      metrics[item]['interestCoverage'] = float(keymetrics[0]['interestCoverage'])

      metrics[item]['Gross_Profit_Margin'] = float(keymetrics[0]['grossProfitMargin'])

      metrics[item]['roe'] = float(keymetrics[0]['returnOnEquity'])

      metrics[item]['priceToSalesRatio'] = float(keymetrics[0]['priceSalesRatio'])
      metrics[item]['price_to_book_Ratio']  = float(keymetrics[0]['priceToBookRatio'])
      metrics[item]['priceEarningsRatio']  = float(keymetrics[0]['priceEarningsRatio'])
      metrics[item]['return_on_assets']  = float(keymetrics[0]['returnOnAssets'])
    except:
      pass

print(metrics)
#outcome
{'AAPL': {'Gross_Profit_Margin': 0.3781776810903472,
  'currentratio': 1.540125617208044,
  'date': '2019-09-28',
  'debtToAssets': 0.7326921031797611,
  'debtToEquity': 2.7410043320661304,
  'dividendYield': 0.012276627402416805,
  'interestCoverage': 17.87751677852349,
  'priceEarningsRatio': 20.81351450883162,
  'priceToSalesRatio': 4.420393881402446,
  'price_to_book_Ratio': 12.709658271815046,
  'return_on_assets': 0.16323009842961633,
  'roe': 0.6106445053487756},
 'ACN': {'Gross_Profit_Margin': 0.30810329734252306,
  'currentratio': 1.3967407576422703,
  'date': '2019-08-31',
  'debtToAssets': 0.5163119824584724,
  'debtToEquity': 1.06744836285.....




metrics_df = pd.DataFrame.from_dict(metrics, orient='index')
metrics_df = metrics_df.T
metrics_df