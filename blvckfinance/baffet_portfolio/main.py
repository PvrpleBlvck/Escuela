import requests
import os
api_key = os.getenv('api_key')


cik = requests.get(f'https://financialmodelingprep.com/api/v3/cik-search/BERKSHIRE HATHAWAY?apikey={api_key}').json()
cik = cik[0]['cik']
print(cik)

latest_filing = requests.get(f'https://financialmodelingprep.com/api/v3/form-thirteen-date/0001035674?apikey={api_key}').json()
latest_filing = latest_filing[0]
print(latest_filing)


form_13 = requests.get(f'https://financialmodelingprep.com/api/v3/form-thirteen/{cik}?date={latest_filing}&apikey={api_key}').json()
print(form_13)
total_portfolio_value = 0
for item in form_13:
  total_portfolio_value = total_portfolio_value + float(item['value'])
print(total_portfolio_value)
allocation = {}
for item in form_13:
  allocation[item['tickercusip']] = {}
  allocation[item['tickercusip']]['value'] = item['value']
  allocation[item['tickercusip']]['perc_position'] = item['value'] / total_portfolio_value
  ticker = item['tickercusip']
  prices = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line&apikey={api_key}').json()
  #price_50_days ago
  try:
    prices_past = prices['historical'][50]['close']
    prices_now = prices['historical'][0]['close']
    return_stock = (prices_now - prices_past)/prices_past
    allocation[item['tickercusip']]['return'] = float(return_stock)
    
  except:
    allocation[item['tickercusip']]['return'] = 0

#calculate total return of our portfolio for the last x days
total_return = 0
for item in allocation:
  total_return = total_return + (allocation[item]['perc_position'] * allocation[item]['return'] )

print(total_return)

#compare with SP500
SP500 = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/^GSPC?serietype=line&apikey={api_key}').json()
SP500_past = SP500['historical'][50]['close']
SP500_today = SP500['historical'][0]['close']
return_sp500 = (SP500_today - SP500_past)/SP500_past
print(return_sp500)