import requests
import numpy as np
import pandas as pd

import os
api_key = os.getenv('api_key')

sectors = ['Technology','Consumer Cyclical','Industrials','Basic Materials','Communication Services','Consumer Defensive','Healthcare','Real Estate','Utilities','Financial','Services']
exchange = 'NASDAQ'
marketcapmorethan = '1000000000'
number_of_companies = 10
symbols = []
overview_Nasdaq = {}


### 1 - request list of tickers for each industry
for sector in sectors:
  symbols = []
  gross_Margin = []
  operating_Margin = []
  net_Profit_Margin = []
  overview_Nasdaq[sector] = {}
  n = 0
  screener = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?{marketcapmorethan}=1000000000&volumeMoreThan=10000&sector={sector}&exchange={exchange}&limit={number_of_companies}&apikey={api_key}').json()
  for item in screener:
    symbols.append(item['symbol'])

### 2 extract Income Statement for each of the companies
  for company in symbols:
    try:
      n = n + 1
      IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&apikey={api_key}').json()

### 3 compute margin ratios and append to list
      gross_Margin.append(IS[0]['grossProfit'] / IS[0]['revenue'])
      operating_Margin.append( (IS[0]['operatingIncome']) / IS[0]['revenue'])
      net_Profit_Margin.append(IS[0]['netIncome'] / IS[0]['revenue'])

    #NP to be able to calculate mean 
    except:
      pass
    gross_Margin = np.array(gross_Margin)
    gross_Margin = np.median(gross_Margin)

    operating_Margin = np.array(operating_Margin) 
    operating_Margin = np.median(operating_Margin)

    net_Profit_Margin = np.array(net_Profit_Margin) 
    net_Profit_Margin = np.median(net_Profit_Margin)

### 4 - Add Ratios to a Dictionary and Convert to Pandas
  
  overview_Nasdaq[sector]['Num. Companies'] = n
  overview_Nasdaq[sector]['Gross Margin'] = gross_Margin * 100
  overview_Nasdaq[sector]['Operating Margin'] = operating_Margin* 100
  overview_Nasdaq[sector]['Net Profit Margin'] = net_Profit_Margin* 100

median_by_Industry = pd.DataFrame.from_dict(overview_Nasdaq,orient='columns')
median_by_Industry

###outcome