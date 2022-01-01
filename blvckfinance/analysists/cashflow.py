import requests
import pandas as pd
import os
api_key = os.getenv('fmpapi_key')

#api_key = api_key

CF = requests.get(f'https://fmpcloud.io/api/v3/cash-flow-statement/AAPL?apikey={api_key}').json()

count= 0
#Create an empty dictionary 
CF_3Y = {}
IS = requests.get(f'https://fmpcloud.io/api/v3/income-statement/AAPL?apikey={api_key}').json()

print(CF)
#outcome
[{'accountsPayables': -1923000000,
  'accountsReceivables': 245000000,
  'acquisitionsNet': -624000000,
  'capitalExpenditure': 10495000000,
  'cashAtBeginningOfPeriod': 25913000000,
  'cashAtEndOfPeriod': 50224000000,
  'changeInWorkingCapital': 42628000000,
  'commonStockIssued': 781000000,
  'commonStockRepurchased': -66897000000,
  'date': '2019-09-28',
  'debtRepayment': -8805000000,
  'deferredIncomeTax': 340000000,
  'depreciationAndAmortization': 12547000000,
  'dividendsPaid': -14119000000,
  'effectOfForexChangesOnCash': 0.0,
  'fillingDate': '2019-10-31',
  'finalLink': 'https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm',
  'freeCashFlow': 58896000000,
  'inventory': -289000000,
  'investmentsInPropertyPlantAndEquipment': -10495000000,
  'link': 'https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.htm',
  'netCashProvidedByOperatingActivites': 69391000000,
  'netCashUsedForInvestingActivites': 45896000000,
  'netCashUsedProvidedByFinancingActivities': -90976000000,
  'netChangeInCash': 24311000000,
  'netIncome': 55256000000,
  'operatingCashFlow': 69391000000,
  'otherFinancingActivites': -1936000000,
  'otherInvestingActivites': 65819000000,
  'otherNonCashItems': 0.0,
  'otherWorkingCapital': 57101000000,
  'period': 'FY',
  'purchasesOfInvestments': -107528000000,
  'salesMaturitiesOfInvestments': 98724000000,
  'stockBasedCompensation': 6068000000,
  'symbol': 'AAPL'},
 {'accountsPayables': 9175000000,





 for item in CF:
  if count < 3:
    date = item['date']
    CF_3Y[date] = item
    #we add revenue as well to the dictionary since we need it to calculate the common-size cash flow
    CF_3Y[date]['Revenue'] = IS[count]['revenue']
    count += 1

print(CF_3Y)
{'2017-09-30': {'Revenue': 229234000000,
  'accountsPayables': 9618000000,
  'accountsReceivables': -2093000000,
  'acquisitionsNet': -329000000,
  'capitalExpenditure': 12795000000,
  'cashAtBeginningOfPeriod': 20484000000,...



CF_Common_Size = pd.DataFrame.from_dict(CF_3Y, orient='index')
CF_Common_Size = CF_Common_Size.T
print(CF_Common_Size)

Revenue = CF_Common_Size.iloc[-1]
CF_Common_Size = CF_Common_Size.iloc[5:-3,:]
CF_Common_Size = (CF_Common_Size/Revenue) * 100

#show as percentage:
pd.options.display.float_format = '{:.2f}%'.format
print(CF_Common_Size)