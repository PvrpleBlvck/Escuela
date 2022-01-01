import requests
import pandas as pd 
import os
api_key = os.getenv('api_key')

companies = ['AMZN','AAPL','MSFT', 'TSLA']
BS_over_time = ''
BS_companies = ''
def balance_sheet(quarter,company,type_analysis):
  #api_key = 'bbb11c6dd9e2948898d127f3f08d94c9'
  BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit=20&apikey={api_key}').json()
  IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&limit=20&apikey={api_key}').json()
  #time analysis
  if type_analysis == 'time':
    BS_metrics = {}
    date = BS[quarter]['date']
    BS_metrics[date] = {}
    BS_metrics[date]['working_capital'] =  BS[quarter]['totalCurrentAssets'] - BS[quarter]['totalCurrentLiabilities']
    BS_metrics[date]['current_ratio'] = BS[quarter]['totalCurrentAssets']/  BS[quarter]['totalCurrentLiabilities']
    BS_metrics[date]['cash_ratio'] =  BS[quarter]['cashAndShortTermInvestments']   / BS[quarter]['totalCurrentLiabilities']
    BS_metrics[date]['LTDebttoEquity'] = ((BS[quarter]['longTermDebt']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[date]['DebttoEquity'] = ((BS[quarter]['totalDebt']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[date]['Financial Leverage'] = ((BS[quarter]['totalAssets']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[date]['Receivable Turnover'] = (IS[quarter]['revenue'] +  IS[quarter+1]['revenue'] + IS[quarter+2]['revenue']+ IS[quarter+3]['revenue']) / ( (BS[quarter]['netReceivables'] + BS[quarter +4]['netReceivables'])/2 )
    BS_metrics[date]['Day_Sales_Outstanding'] = 365 /BS_metrics[date]['Receivable Turnover']
    BS_metrics[date]['Inventory_Turnover'] = (IS[quarter]['costOfRevenue'] +  IS[quarter+1]['costOfRevenue'] + IS[quarter+2]['costOfRevenue']+ IS[quarter+3]['costOfRevenue'])/ ( (BS[quarter]['inventory'] + BS[quarter +4]['inventory'])/2 )
    BS_metrics[date]['DOH'] = 365 / BS_metrics[date]['Inventory_Turnover']
    BS_metrics[date]['Asset_Turnover'] = (IS[quarter]['revenue'] +  IS[quarter+1]['revenue'] + IS[quarter+2]['revenue']+ IS[quarter+3]['revenue']) / ( (BS[quarter]['totalAssets'] + BS[quarter +4]['totalAssets'])/2 )
    return BS_metrics
  else:
    BS_metrics = {}
    #date = BS[quarter][company]
    BS_metrics[company] = {}
    BS_metrics[company]['working_capital'] =  BS[quarter]['totalCurrentAssets'] - BS[quarter]['totalCurrentLiabilities']
    BS_metrics[company]['current_ratio'] = BS[quarter]['totalCurrentAssets']/  BS[quarter]['totalCurrentLiabilities']
    BS_metrics[company]['cash_ratio'] =  BS[quarter]['cashAndShortTermInvestments']   / BS[quarter]['totalCurrentLiabilities']
    BS_metrics[company]['LTDebttoEquity'] = ((BS[quarter]['longTermDebt']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[company]['DebttoEquity'] = ((BS[quarter]['totalDebt']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[company]['Financial Leverage'] = ((BS[quarter]['totalAssets']  ) / BS[quarter]['totalStockholdersEquity'])
    BS_metrics[company]['Receivable Turnover'] = (IS[quarter]['revenue'] +  IS[quarter+1]['revenue'] + IS[quarter+2]['revenue']+ IS[quarter+3]['revenue']) / ( (BS[quarter]['netReceivables'] + BS[quarter +4]['netReceivables'])/2 )
    BS_metrics[company]['Day_Sales_Outstanding'] = 365 /BS_metrics[company]['Receivable Turnover']
    BS_metrics[company]['Inventory_Turnover'] = (IS[quarter]['costOfRevenue'] +  IS[quarter+1]['costOfRevenue'] + IS[quarter+2]['costOfRevenue']+ IS[quarter+3]['costOfRevenue'])/ ( (BS[quarter]['inventory'] + BS[quarter +4]['inventory'])/2 )
    BS_metrics[company]['DOH'] = 365 / BS_metrics[company]['Inventory_Turnover']
    BS_metrics[company]['Asset_Turnover'] = (IS[quarter]['revenue'] +  IS[quarter+1]['revenue'] + IS[quarter+2]['revenue']+ IS[quarter+3]['revenue']) / ( (BS[quarter]['totalAssets'] + BS[quarter +4]['totalAssets'])/2 )
    return BS_metrics


if len(companies) == 1:
  #Time Serie Analysis
  print(companies[0])
  recent_BS = balance_sheet(0,companies[0],'time')
  one_quarter_ago = balance_sheet(1,companies[0],'time') 
  two_quarter_ago = balance_sheet(2,companies[0],'time')
  three_quarter_ago = balance_sheet(3,companies[0],'time')
  four_quarter_ago = balance_sheet(4,companies[0],'time')
  Balance_sheet_all = []
  Balance_sheet_all.append(recent_BS)
  Balance_sheet_all.append(one_quarter_ago)
  Balance_sheet_all.append(two_quarter_ago)
  Balance_sheet_all.append(three_quarter_ago)
  Balance_sheet_all.append(four_quarter_ago)
  Balance_sheet_all
  #convert nested dictionaries to dataframe
  BS_over_time = pd.concat([pd.DataFrame(l) for l in Balance_sheet_all],axis=1).T
#Cross Company Analysis
else:
  Balance_sheet_all = []
  for company in companies:
    BS_company = balance_sheet(0,company,'')
    Balance_sheet_all.append(BS_company)
  BS_companies = pd.concat([pd.DataFrame(l) for l in Balance_sheet_all],axis=1).T


print(BS_companies)
print(BS_over_time)