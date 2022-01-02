import requests
import pandas as pd

technological_companies = ['MSFT','AAPL','AMZN','GOOG','IBM','CSCO','ORCL','SAP','IBM']
companies = technological_companies
all_Receivables = {} 


for company in companies:
  try:
    balanceSheet = requests.get(f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{company}?period=quarter')
    balanceSheet = balanceSheet.json()
    all_Receivables[company] = {}
    for item in balanceSheet['financials']:
      receivables = item['Receivables']
      all_Receivables[company]['receivables'] = receivables

    IS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?period=quarter')
    IS = IS.json()
    for item in IS['financials']:
      revenues = item['Revenue']
      all_Receivables[company]['Revenue'] = revenues
    
    all_Receivables[company]['receivables_to_sales'] = float(receivables)/float(revenues)
  except:
    pass


receivables_companies = pd.DataFrame.from_dict(all_Receivables, orient='index')
receivables_companies = receivables_companies.T

receivables_companies = receivables_companies[receivables_companies.index =='receivables_to_sales'] 
receivables_companies = receivables_companies.T.reset_index()

import plotly.express as px
fig = px.bar(receivables_companies, x=receivables_companies['index'],y =receivables_companies['receivables_to_sales'])
fig.show()