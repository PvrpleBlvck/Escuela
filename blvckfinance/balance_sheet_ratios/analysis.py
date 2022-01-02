import os
api_key = os.getenv('api_key')



companies = ['ABBV', 'AGN', 'JNJ', 'LLY', 'MRK', 'MYL', 'PRGO', 'PFE', 'ZTS']
assets = []
liabilities = []
equity = []
#api_key = 'your api key'
import requests

for company in companies:
  
    Balance_Sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit=1&apikey={api_key}")

    Balance_Sheet = Balance_Sheet.json()
    #print(Balance_Sheet)
    
    asset_i = Balance_Sheet[0]['totalAssets']
    assets.append(asset_i)
    
    liabilities_i = Balance_Sheet[0]['totalLiabilities']
    liabilities.append(liabilities_i)
    
    equity_i = Balance_Sheet[0]['totalStockholdersEquity']
    equity.append(equity_i)

import plotly.graph_objects as go

firms = companies
#companies contains our list of firms e.g. ['ABBV', 'AGN'..]

fig = go.Figure(data=[
    go.Bar(name='Assets', x=companies, y=assets ),
    go.Bar(name='Liabilities', x=companies, y=liabilities),
    go.Bar(name='Equity', x=companies, y=equity)
])

fig.update_layout(barmode='stack',title = 'Balance Sheet Latest Quarter')
fig.show()