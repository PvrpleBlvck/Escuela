import requests
import numpy as np
import pandas as pd
import os
api_key = os.getenv('api_key')

demo = api_key

sector = 'Technology'
exchange = 'NASDAQ'
marketcapmorethan = '1000000000'
number_of_companies = 100
symbols = []

screener = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?{marketcapmorethan}=1000000000&volumeMoreThan=10000&sector={sector}&exchange={exchange}&limit={number_of_companies}&apikey={demo}').json()
for item in screener:
  symbols.append(item['symbol'])



FinMetrics = {}
for company in symbols:
  try:
    companydata = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey={demo}').json()
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&apikey={demo}').json()
    BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&apikey={demo}').json()
    CF = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?period=quarter&apikey={demo}').json()
    #revenue last 4 years
    revenue = [IS[0]['revenue'],IS[1]['revenue'],IS[2]['revenue'],IS[3]['revenue']]
    revenue = np.array(revenue).sum()
    net_income = [IS[0]['netIncome'],IS[1]['netIncome'],IS[2]['netIncome'],IS[3]['netIncome']]
    net_income = np.array(net_income).sum()

    FCF = CF[0]['freeCashFlow'] + CF[1]['freeCashFlow'] + CF[2]['freeCashFlow'] + CF[3]['freeCashFlow']
    OperatingCF = CF[0]['operatingCashFlow'] + CF[1]['operatingCashFlow'] + CF[2]['operatingCashFlow'] + CF[3]['operatingCashFlow']
    total_debt = BS[0]['totalDebt']

    eps_diluted = [IS[0]['epsdiluted'],IS[1]['epsdiluted'],IS[2]['epsdiluted'],IS[3]['epsdiluted']]
    eps_diluted = np.array(eps_diluted).sum()
  
    total_shareholders_equity = BS[0]['totalStockholdersEquity']
    shareholders_equity_2_quarters_Average = (BS[0]['totalStockholdersEquity'] + BS[1]['totalStockholdersEquity']) / 2

    total_assets_2qts = (BS[0]['totalAssets'] + BS[1]['totalAssets']) / 2

    latest_Annual_Dividend = companydata[0]['lastDiv']
    price = companydata[0]['price']
    market_Capitalization = companydata[0]['mktCap']
    name = companydata[0]['companyName']
    exchange = companydata[0]['exchange']
    EBITDATTM = IS[0]['ebitda'] + IS[1]['ebitda'] + IS[2]['ebitda'] + IS[3]['ebitda']
    EBITDA5YTTM = IS[20]['ebitda'] + IS[21]['ebitda'] + IS[22]['ebitda'] + IS[23]['ebitda']
    EBITDA5YGrowht = (( EBITDATTM - EBITDA5YTTM) / EBITDA5YTTM)*100

    grossprofitma12TTMgrowht = ((IS[0]['grossProfitRatio'] - IS[3]['grossProfitRatio']) / IS[3]['grossProfitRatio']) *100

    dividend_Yield= latest_Annual_Dividend/price
    FinMetrics[company] = {}
    FinMetrics[company]['Dividend_Yield'] = dividend_Yield * 100
    FinMetrics[company]['latest_Price'] = price
    FinMetrics[company]['latest_Dividend'] = latest_Annual_Dividend
    FinMetrics[company]['market_Capit_in_M'] = market_Capitalization/1000000
    FinMetrics[company]['pe'] = price / eps_diluted
    FinMetrics[company]['ps'] = market_Capitalization / revenue
    FinMetrics[company]['pb'] = market_Capitalization / total_shareholders_equity
    FinMetrics[company]['PEG'] = FinMetrics[company]['pe'] / EBITDA5YGrowht
    FinMetrics[company]['GPM'] = IS[0]['grossProfitRatio']
    FinMetrics[company]['latest_Financials'] = IS[0]['date']
    FinMetrics[company]['GPM12TTMGrowth'] = grossprofitma12TTMgrowht
    FinMetrics[company]['Revenue_last6qts_inM'] = [IS[0]['revenue'],IS[1]['revenue'],IS[2]['revenue'],IS[3]['revenue'],IS[4]['revenue'],IS[5]['revenue']]
    FinMetrics[company]['Revenue_last6qts_inM'] = np.array(FinMetrics[company]['Revenue_last6qts_inM']) / 1000000
    FinMetrics[company]['ptoOperatingCF'] = market_Capitalization / OperatingCF

    FinMetrics[company]['ptoFCF'] = market_Capitalization / FCF
    FinMetrics[company]['Debt_to_Equity'] = total_debt / total_shareholders_equity
    FinMetrics[company]['ROE'] = net_income / shareholders_equity_2_quarters_Average
    FinMetrics[company]['ROA'] = net_income / total_assets_2qts

    FinMetrics[company]['revenue_growht_4qrts'] = ((IS[0]['revenue'] -  IS[3]['revenue'])/ IS[3]['revenue']) *100
    FinMetrics[company]['earnings_growht_4qrts'] = ((IS[0]['netIncome'] -  IS[3]['netIncome'])/ IS[3]['netIncome']) *100

  except:
    pass


all_measures= pd.DataFrame.from_dict(FinMetrics,orient='index')
print(all_measures.head(5))


#keep only companies with a PE higher than 10
price_earnings = all_measures[all_measures['pe'] > 0]

#filter option 1
price_earnings = price_earnings[(price_earnings['pe'] < 30) & (price_earnings['ps'] < 20) & (price_earnings['pb'] < 20) & (price_earnings['ptoFCF'] < 20)]

#filter option 2
#price_earnings = price_earnings[(price_earnings['pe'] < 20) & (price_earnings['revenue_growht_4qrts'] > 10)]

#Sort entities to show companies with lower PE ratio first
price_earnings = price_earnings.sort_values('pe')
#keep only 8 companies:
price_earnings = price_earnings[0:8]

#calculate industry median for each of the ratios: 
price_earnings.loc[-1] = all_measures.median()
#rename the column
price_earnings.rename(index={-1: "median_industry"},inplace=True)

print(price_earnings)

price_earnings[['pe','ps','pb','PEG','ptoFCF']].plot()
price_earnings[['Dividend_Yield','revenue_growht_4qrts']].plot(kind="bar")