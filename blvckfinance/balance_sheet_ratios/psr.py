import requests 
import pandas as pd

import requests

import os
api_key = os.getenv('fmpapi_key')
companies = requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector=technology&marketCapMoreThan=100000000000&limit=100&apikey={apikey}')
companies = companies.json()

technological_companies = []

for item in companies:
  technological_companies.append(item['symbol'])

print(technological_companies)
#['MSF.BR', 'MSFT', 'AAPL', 'AMZN', 'GOOG', 'GOOGL', 'FB', 'INCO.BR', 'INTC', ...



pricetosales = {}
for item in technological_companies:
    try:
      #annual income statement since we need anual sales
      IS = requests.get(f'https://fmpcloud.io/api/v3/income-statement/{item}?apikey={api_key}')
      IS = IS.json()
      Revenue = IS[0]['revenue']
      grossprofitratip = IS[0]['grossProfitRatio']
      #most recent market capitliazation
      MarketCapit = requests.get(f'https://fmpcloud.io/api/v3/market-capitalization/{item}?apikey={api_key}')
      MarketCapit = MarketCapit.json()
      MarketCapit = MarketCapit[0]['marketCap']

      #Price to sales
      p_to_sales = MarketCapit/Revenue

      pricetosales[item] = {}
      pricetosales[item]['revenue'] = Revenue
      pricetosales[item]['Gross_Profit_ratio'] = grossprofitratip
      pricetosales[item]['price_to_sales'] = p_to_sales
      pricetosales[item]['Market_Capit'] = MarketCapit
    except:
      pass

print(pricetosales)
#
{'AAPL': {'Gross_Profit_ratio': 0.37817768109,
  'Market_Capit': 1075385951640,
  'price_to_sales': 4.133333659935274,
  'revenue': 260174000000},
 'ADBE': {'Gross_Profit_ratio': 0.850266267202,
  'Market_Capit': 143222958000,
  'price_to_sales': 12.820620380963822,
  'revenue': 11171297000},
 'AMZN': {'Gross_Profit_ratio': 0.409900114786,
  'Market_Capit': 960921360000

price_to_sales_df = pd.DataFrame.from_dict(pricetosales, orient='index')
price_to_sales_df['ps_average_sector'] = price_to_sales_df['price_to_sales'].mean()
price_to_sales_df['pscompany_vs_averagesector'] = price_to_sales_df['price_to_sales'] - price_to_sales_df['ps_average_sector']
price_to_sales_df['price_as_per_average_industryPS'] = price_to_sales_df['ps_average_sector'] * price_to_sales_df['revenue']
price_to_sales_df['price_difference'] = price_to_sales_df['price_as_per_average_industryPS'] - price_to_sales_df['Market_Capit']