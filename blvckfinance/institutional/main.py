import requests 
import pandas as pd

companies = ['AAPL','MSFT','ETSY','ATVI']
change = {}

for company in companies:
	institutions = requests.get(f'https://financialmodelingprep.com/api/v3/institutional-holder/{company}?apikey=bbb11c6dd9e2948898d127f3f08d94c9').json()
	change[company] = {}
	identify = 0
	count_down = 0
	count_up = 0
	total_shares_exchanged = 0
	for item in institutions:
		identify = identify + 1
		if item['dateReported'] > '2021-12-11':
			change[company][item['dateReported']+ str(identify)] = item['change']
			if item['change'] > 0:
				count_up = count_up + 1
			if item['change'] < 0:
				count_down = count_down + 1
			total_shares_exchanged = total_shares_exchanged + item['change']

	change[company]['total'] = count_up + count_down
	change[company]['buys'] = count_up
	change[company]['sells'] = count_down
	change[company]['total_shares_exchanged'] = total_shares_exchanged

institutions_DF = pd.DataFrame(change)
institutions_DF = institutions_DF.T 

print(institutions_DF[['total','buys','sells','total_shares_exchanged']])