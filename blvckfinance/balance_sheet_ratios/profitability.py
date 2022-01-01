import requests
import pandas as pd 
stock = 'AAPL'

import os
api_key = os.getenv('api_key')

url = f'https://financialmodelingprep.com/api/v4/stock_peers?symbol={stock}&apikey={api_key}'

#1 GET LIST OF PEERS
peers = requests.get(url).json()
peers = peers[0]['peersList']

profitability_ratios = {}
#2 Retrieve Profitability Ratios for each of the peers
for stock in peers:
  #3 Add to Python Dictionary
  profitability_ratios[stock] = {}
  fr = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{stock}?apikey={api_key}'
  financial_ratios_ttm = requests.get(fr).json()
  profitability_ratios[stock]['Return on Assets'] = financial_ratios_ttm[0]['returnOnAssetsTTM']
  profitability_ratios[stock]['Return on Equity'] = financial_ratios_ttm[0]['returnOnEquityTTM']
  profitability_ratios[stock]['Gross Profit Margin'] = financial_ratios_ttm[0]['grossProfitMarginTTM']
  profitability_ratios[stock]['Opearting Profit Margin'] = financial_ratios_ttm[0]['operatingProfitMarginTTM']
  profitability_ratios[stock]['Net Profit Margin'] = financial_ratios_ttm[0]['netProfitMarginTTM']

#4 Convert into Pandas DataFrame
profitability_ratios = pd.DataFrame(profitability_ratios)
profitability_ratios