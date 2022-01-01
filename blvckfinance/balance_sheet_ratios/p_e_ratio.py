import pandas as pd
import requests
import os
api_key = os.getenv('api_key')


company = 'MSFT'
eps = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?limit=12&apikey={api_key}').json()
eps = eps[:8]

analysis_data = {}
for item in eps:
  analysis_data[item['date']] = {}
  analysis_data[item['date']]['eps'] =  item['epsdiluted']
  
analysis_data

key_metrics = requests.get(f'https://financialmodelingprep.com/api/v3/key-metrics/{company}?limit=10&apikey={api_key}').json()
key_metrics = key_metrics[:8]
for item in key_metrics:
  analysis_data[item['date']]['BVPS'] = item['bookValuePerShare']
  analysis_data[item['date']]['ROE'] = item['roe']
  analysis_data[item['date']]['PE'] = item['peRatio']


normalized_EPS = pd.DataFrame(analysis_data)
normalized_EPS

normalize_mean = normalized_EPS.mean(axis=1)
eps_average = normalize_mean['eps']
roe_average = normalize_mean['ROE']
latest_BVPS = normalized_EPS.iloc[1:2,0][0]

price= requests.get(f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey={api_key}').json()
price = price[0]['price']

PEnormalized_average_eps = price/eps_average
print(PEnormalized_average_eps)

normalized_eps_average_ROE = roe_average*latest_BVPS
PEnormalized_ROE_EPS = price/normalized_eps_average_ROE
print(PEnormalized_ROE_EPS)