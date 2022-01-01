import requests
import pandas as pd

import os
api_key = os.getenv('api_key')

stock = 'AAPL'
BS = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?apikey={api_key}").json()
BS2016 = BS[3]
BS2017 = BS[2]
BS2018 = BS[1]
BS2019= BS[0]

IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={demo}').json()
IS2017 = IS[2]
IS2018 = IS[1]
IS2019 = IS[0]


#Element 1 net income / sales as profitability indicator:
Profitability2017 = IS2017['netIncome']/IS2017['revenue']
Profitability2018 = IS2018['netIncome']/IS2018['revenue']
Profitability2019 = IS2019['netIncome']/IS2019['revenue']

#Element 2 Technical Analysis
TechnicalEfficiency2017 = IS2017['revenue']/((BS2017['totalAssets'] + BS2016['totalAssets'])/2)
TechnicalEfficiency2018 = IS2018['revenue']/((BS2018['totalAssets'] + BS2017['totalAssets'])/2)
TechnicalEfficiency2019 = IS2019['revenue']/((BS2019['totalAssets'] + BS2018['totalAssets'])/2)

#Element 3 Firm Financial Structure
FinancialStructure2017 = ((BS2017['totalAssets'] + BS2016['totalAssets'])/2)/  ((BS2017['totalStockholdersEquity'] + BS2016['totalStockholdersEquity'] )/2)
FinancialStructure2018 = ((BS2018['totalAssets'] + BS2017['totalAssets'])/2)/ ((BS2018['totalStockholdersEquity'] + BS2017['totalStockholdersEquity'] )/2)
FinancialStructure2019 = ((BS2019['totalAssets'] + BS2018['totalAssets'])/2)/((BS2019['totalStockholdersEquity'] + BS2018['totalStockholdersEquity'] )/2)


ROE2017 = Profitability2017 * TechnicalEfficiency2017 * FinancialStructure2017
ROE2018= Profitability2018 * TechnicalEfficiency2018 * FinancialStructure2018
ROE2019 = Profitability2019 * TechnicalEfficiency2019 * FinancialStructure2019

FY2017 = [Profitability2017,TechnicalEfficiency2017,FinancialStructure2017,ROE2017]
FY2018 = [Profitability2018,TechnicalEfficiency2018,FinancialStructure2018,ROE2018]
FY2019 = [Profitability2019,TechnicalEfficiency2019,FinancialStructure2019,ROE2019]

ROE_decomposition = pd.DataFrame([FY2017,FY2018, FY2019],columns=['Profitability *','Tech Efficiency *','Financial Strucutre =','ROE'],index=['2017','2018','2019'])

print(ROE_decomposition)
