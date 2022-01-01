import pandas as pd
import requests
import json

import os
api_key = os.getenv('api_key')

def financialratios(quote):
   fr = requests.get(f"https://financialmodelingprep.com/api/v3/financial-ratios/{quote}?apikey={api_key}")
fr = fr.json()


valuation = fr['ratios'][0]['investmentValuationRatios']
  profitability = fr['ratios'][0]['profitabilityIndicatorRatios']
  operating = fr['ratios'][0]['operatingPerformanceRatios']
  liquidity = fr['ratios'][0]['liquidityMeasurementRatios']
  debt = fr['ratios'][0]['debtRatios']
  valuation = pd.DataFrame(list(valuation.items()),columns=['Ratio', quote])
  profitability = pd.DataFrame(list(profitability.items()),columns=['Ratio', quote])
  operating = pd.DataFrame(list(operating.items()),columns=['Ratio', quote])
  liquidity = pd.DataFrame(list(liquidity.items()),columns=['Ratio', quote])
  debt = pd.DataFrame(list(debt.items()),columns=['Ratio', quote])


frames = [valuation,profitability,operating,liquidity,debt]
  result = pd.concat(frames)
  return result


listofstocks = ['AAPL','MSFT','FB','TSLA']
x = financialratios('GOOGL')

for item in listofstocks:
    y = financialratios(item)
    x = x.merge(y,on='Ratio')