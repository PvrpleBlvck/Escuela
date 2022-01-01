import requests
import os
api_key = os.getenv('fmpapi_key')

demo= api_key

companies = requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector=technology&marketCapMoreThan=100000000000&limit=100&apikey={demo}')
companies = companies.json()

technological_companies = []

for item in companies:
  technological_companies.append(item['symbol'])

print(technological_companies)
#outcome
['MSFT',
 'MSF.BR',
 'AAPL',
 'AMZN',...]


 # API ENDPOINT https://fmpcloud.io/api/v3/balance-sheet-statement/AAPL?period=quarter&apikey=demo

liquidity_measures = {}
for item in technological_companies:
  try:
    BS = requests.get(f'https://fmpcloud.io/api/v3/balance-sheet-statement/{item}?period=quarter&apikey={demo}')
    BS = BS.json()
   
    #Working Capital Calculation and Current Ratio
    current_Assets = BS[0]['totalCurrentAssets']
    current_Liabilities = BS[0]['totalCurrentLiabilities']
    working_Capital = current_Assets - current_Liabilities
    current_Ratio = (current_Assets/current_Liabilities)

    #Quick ratio calculation
    cash = BS[0]['cashAndCashEquivalents']
    marketable_Securities =  BS[0]['cashAndShortTermInvestments']
    receivables = BS[0]['netReceivables']
    quick_Ratio = (cash + marketable_Securities + receivables )/current_Liabilities

    #Cash ratio calculation
    cash_Ratio = (cash + marketable_Securities) / current_Liabilities

    #store liquidity ratios for each company to liquidity_measures dictionary
    liquidity_measures[item] = {}
    liquidity_measures[item]['working_capital'] = working_Capital
    liquidity_measures[item]['current_ratio'] = current_Ratio
    liquidity_measures[item]['quick_ratio'] = quick_Ratio
    liquidity_measures[item]['cash_ratio'] = quick_Ratio
  except:
    pass

print(liquidity_measures)
{'AAPL': {'cash_ratio': 1.6435136695999453,
  'current_ratio': 1.5977819324399722,
  'quick_ratio': 1.6435136695999453,
  'working_capital': 61070000000},
 'ACN': {'cash_ratio': 1.669638718595044,
  'current_ratio': 1.378232129956632,
  'quick_ratio': 1.669638718595044,
  
...




import pandas as pd

#Convert dictionary with company liquidity ratios into a Pandas DataFrame:

liquidity_dataframe = pd.DataFrame.from_dict(liquidity_measures, orient='index')

print(liquidity_dataframe)

  working_capital current_ratio quick_ratio cash_ratio
MSFT  1.074340e+11  2.801375  2.794131  2.794131
AAPL  6.107000e+10  1.597782  1.643514  1.643514
AMZN  8.522000e+09  1.097048  1.274644  1.274644
GOOGL 1.073570e+11  3.374052  3.615555  3.615555

#Calculate the mean 
print(liquidity_dataframe['current_ratio'].mean())
#2.6494566821574446