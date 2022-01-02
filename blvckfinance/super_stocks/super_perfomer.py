stocks = pd.read_csv('all_stocks_SP500.csv')
stocks = stocks.T
stocks.columns = stocks.iloc[0]
stocks = stocks[1:]
stocks['condition1'] = (stocks['price'] > stocks['200 MA']) & (stocks['price'] > stocks['150 MA'])

stocks['condition2'] = stocks['150 MA'] > stocks['200 MA']
#3 The 200-day moving average line is trending up for 1 month 
stocks['condition3'] = stocks['200 MA'] > stocks['200 MA_1mago']
stocks['condition4'] = (stocks['50 MA'] > stocks['200 MA']) & (stocks['50 MA'] > stocks['150 MA'])
stocks['condition5'] = stocks['price'] > stocks['50 MA']
#6 The current stock price is at least 30 percent above its 52-week low
stocks['condition6'] = stocks['price'] > stocks['Above_30%_low']
#7 The current stock price is within at least 25 percent of its 52-week high.
stocks['condition7'] = stocks['price'] > stocks['Within_25%_high']
#8 The relative strength ranking is above 80
stocks['condition8'] = stocks['pct_rank'] > 0.8

selection = stocks[(stocks['condition1'] == True) & (stocks['condition2'] == True) & (stocks['condition3'] == True) & (stocks['condition4'] == True)
		& (stocks['condition5'] == True) & (stocks['condition6'] == True) & (stocks['condition7'] == True) & (stocks['condition8'] == True)]

print(selection)