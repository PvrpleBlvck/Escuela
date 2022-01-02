import requests
import pandas as pd

import os
api_key = os.getenv('api_key')


stock = 'AAPL'
IS = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&apikey={apikey}").json()

print(IS)

[{'acceptedDate': '2020-07-30 19:29:09',
  'costAndExpenses': 33133000000,
  'costOfRevenue': 37005000000,
  'date': '2020-06-27',
  'depreciationAndAmortization': 2752000000,
  'ebitda': 1



#in the API we can find the op profit as Operating Income
operating_Profit = IS[0]['operatingIncome'] 
EBT = IS[0]['incomeBeforeTax']

financialLeverage = operating_Profit/ EBT
print(financialLeverage)