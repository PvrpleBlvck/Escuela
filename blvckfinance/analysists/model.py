import requests
import pandas as pd
import os
api_key = os.getenv('api_key')

companies = []
demo = api_key

marketcap = str(1000000000)

url = (f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={marketcap}&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=1000&apikey={demo}')

#get companies based on criteria defined about
screener = requests.get(url).json()
print(screener)

[{'symbol': 'AAPL', 'companyName': 'Apple Inc.', 'marketCap': 1526030790000, 'sector': 'Technology', 'beta': 1.228499, 'pri
ce': 352.08, 'lastAnnualDividend': 3.08, 'volume': 42532806, 'exchange': 'Nasdaq Global Select', 'exchangeShortName': 'NASD
AQ'}, {'symbol': 'MSFT', 'companyName':....


#add selected companies to a list
for item in screener:
	companies.append(item['symbol'])
	
#print(companies)

value_ratios ={}
#get the financial ratios
count = 0
for company in companies:
	try:
		if count <30:
			count = count + 1
			fin_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
			value_ratios[company] = {}
			value_ratios[company]['ROE'] = fin_ratios[0]['returnOnEquity']
			value_ratios[company]['ROA'] = fin_ratios[0]['returnOnAssets']
			value_ratios[company]['Debt_Ratio'] = fin_ratios[0]['debtRatio']
			value_ratios[company]['Interest_Coverage'] = fin_ratios[0]['interestCoverage']
			value_ratios[company]['Payout_Ratio'] = fin_ratios[0]['payoutRatio']
			value_ratios[company]['Dividend_Payout_Ratio'] = fin_ratios[0]['dividendPayoutRatio']
			value_ratios[company]['PB'] = fin_ratios[0]['priceToBookRatio']
			value_ratios[company]['PS'] = fin_ratios[0]['priceToSalesRatio']
			value_ratios[company]['PE'] = fin_ratios[0]['priceEarningsRatio']
			value_ratios[company]['Dividend_Yield'] = fin_ratios[0]['dividendYield']
			value_ratios[company]['Gross_Profit_Margin'] = fin_ratios[0]['grossProfitMargin']
			#more financials on growth:https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=demo
			growth_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/financial-growth/{company}?apikey={demo}').json()
			value_ratios[company]['Revenue_Growth'] = growth_ratios[0]['revenueGrowth']
			value_ratios[company]['NetIncome_Growth'] = growth_ratios[0]['netIncomeGrowth']
			value_ratios[company]['EPS_Growth'] = growth_ratios[0]['epsgrowth']
			value_ratios[company]['RD_Growth'] = growth_ratios[0]['rdexpenseGrowth']
								
	except:
		pass
print(value_ratios)


Value Ratio Dictionary outcome:
{'AAPL': {'ROE': 0.6106445053487756, 'ROA': 0.16323009842961633, 'Debt_Ratio': 0.7326921031797611, 'Interest_Coverage': 18.382829977628635, 'Payout_Ratio': 0.25551976255972203, 'Dividend_Payout_Ratio': 0.25551976255972203, 'PB': 12.709658271815046, 'PS': 4.420393881402446, 'PE': 20.81351450883162, 'Dividend_Yield': 0.012276627402416805, 'Gross_Profit_Margin': 0.3781776810903472, 'Revenue_Growth': -0.020410775805267418, 'NetIncome_Growth': -0.07181132519191681, 'EPS_Growth': -0.003330557868442893, 'RD_Growth': 0.1391542568137117}, 'MSFT': {'ROE': 0.3834652594547054, 'ROA': 0.13693658482111698, 'Debt_Ratio': 0.6428970253632798, 'Interest_Coverage': 5.881980640357408, 'Payout_Ratio':0.35196228338430174, 'Dividend_Payout_Ratio': 0.3519622833843017, 'PB': 10.52384979966774, 'PS': 8.557532401484389, 'PE': 27.444076197757386, 'Dividend_Yield': 0.012824708722134454, 'Gross_Profit_Marg


DF = pd.DataFrame.from_dict(value_ratios,orient='index')
print(DF.head(4))

          ROE       ROA  Debt_Ratio  Interest_Coverage  Payout_Ratio  ...  Gross_Profit_Margin  Revenue_Growth  NetIncome_Growth  EPS_Growth  RD_Growth
AAPL  0.610645  0.163230    0.732692          18.382830      0.255520  ...             0.378178       -0.020411         -0.071811   -0.003331   0.139154
ADBE  0.280286  0.142154    0.492826          20.384578      0.000000  ...             0.850266        0.237130          0.139219    0.149621   0.255178
ADI   0.116405  0.063714    0.452653           6.485771      0.570414  ...             0.669956       -0.033846         -0.088550   -0.080605  -0.030086
ADSK -1.542056  0.034713    1.022511                NaN      0.000000  ...             0.900773        0.274146         -3.654703   -3.648649   0.173931


#mean to enable comparison across ratios
ratios_mean = []
for item in DF.columns:
	ratios_mean.append(DF[item].mean())

#divide each value in dataframe by mean to normalize values
DF = DF / ratios_mean

DF['ranking'] = DF['NetIncome_Growth']*Net_Income_Growth + DF['Revenue_Growth']*Revenue_Growth  + DF['ROE']*ROE + DF['ROA']*ROA + DF['Debt_Ratio'] * Debt_Ratio + DF['Interest_Coverage'] * Interest_Coverage + DF['Dividend_Payout_Ratio'] * Dividend_Payout_Ratio + DF['PB']*PB + DF['PS']*PS 

print(DF.sort_values(by=['ranking'],ascending=False))