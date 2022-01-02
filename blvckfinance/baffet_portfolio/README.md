Note that we need to have an API key in order for the code to run. You can add yours within below api_key variable:

import requests
api_key = 'your api key'
cik = requests.get(f'https://financialmodelingprep.com/api/v3/cik-search/BERKSHIRE HATHAWAY?apikey={api_key}').json()
cik = cik[0]['cik']
print(cik)
#outcome 
0001067983
After running the code, we can see that the cik for Berkshire is 0001067983.

Next, we identify all filings available for our selected cik. As mentioned before, each quarter Berkshire Hathaway is due to make public its holdings using Form 13. In this post, we will only use the most recent filing. To find all available filings, we can run below code. Note that we pass the cik as part of the url and extract the first element on the returned list since that will be the latest filing.

latest_filing = requests.get(f'https://financialmodelingprep.com/api/v3/form-thirteen-date/{cik}?apikey={api_key}').json()
latest_filing = latest_filing[0]
print(latest_filing)
#outcome 2021-06-30
As shown above, the most up to date filing available is from June 2021 (i.e. the returned date is 2021-06-30). We will use the date in the next piece of code in order to retrieve all Warren Buffett stocks as per June 2021.
Finally, we can retrieve all positions held by Warren Buffett’s in its company portfolio in June 2021:

form_13 = requests.get(f'https://financialmodelingprep.com/api/v3/form-thirteen/{cik}?date={latest_filing}&apikey={api_key}').json()
print(form_13)


#outcome
[{'date': '2021-06-30', 'fillingDate': '2021-08-16', 'acceptedDate': '2021-08-16 16:02:07', 'cik': '0001067983', 'cusip': '037833100', 'tickercusip': 'AAPL', 'nameOfIssuer': 'APPLE INC', 'shares': 887135554, 'titleOfClass': 'COM', 'value': 121502087000...
If we look at the outcome above, we see a Python list where each element represents a stock position, i.e. First stock in the list is Apple. The biggest position in Berkshire’s portfolio.

In the next section, we are going to extract price data required to calculate the return of Warren Buffett’s portfolio.

Calculating Warren Buffett Portfolio returns
To calculate Berkshire Hathaway portfolio returns, we are going to create a Python dictionary to add the stock ticker and value of each of the positions. With this information, we can calculate Buffett’s portfolio allocation per stock as per the total value of the portfolio, using the total value of the portfolio. This will allow us to compute the total return.

We start by calculating the total Berkshire’s portfolio value:

total_portfolio_value = 0
#1 Loop through each of the positions and compute total portfolio value
for item in form_13:
 total_portfolio_value = total_portfolio_value + float(item['value'])
print(total_portfolio_value)
#outcome
293023412000.0
Next, we create a Python dictionary to add all information for each of the tickers. Note that the nested dictionary contains as a key the stock ticker. That way, we can store below additional data for each stock:

Value of the position
Allocation of the position as per total value of the portfolio
To calculate the return, we need the price of the stock 50 days ago and the price of the stock today. For our strategy, we will assume that we hold the stock 50 days so that is the base used to calculate the return
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
print(allocation)
 
Below screenshot shows how the allocation dictionary should look like. We can observe the return and the percentage of the position as of the total portfolio. For instance, Apple represents 41% of the total portfolio in Warren Buffett’s portfolio. And the return in the last 50 days for this position is of around 1%.



Comparing Warren Buffett portfolio returns to market returns:
To backtest how good the strategy of replicating Warren Buffett’s portfolio is, we assume that we buy and hold the stocks for 50 days. 

#calculate total return of portfolio for the last 50 days

total_return = 0
for item in allocation:
 total_return = total_return + (allocation[item]['perc_position'] * allocation[item]['return'] )
 
print(total_return)
#outcome
-0.005689237724399295
The total return of this strategy is negative. So we would have lost money if we were to replicate Warren Buffett’s portfolio and hold the stocks for 50 days. However, to know if it is a good strategy or not, we should use a benchmark. It may be that our strategy yields a negative return but the S&P 500 (a market index) performed even worse. Let’s find out.

We can compare Warren’s replication return to a portfolio’s return consisting of buying and holding the S&P 500 for 50 days:

#compare with SP500

SP500 = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/^GSPC?serietype=line&apikey={api_key}').json()
SP500_past = SP500['historical'][50]['close']
SP500_today = SP500['historical'][0]['close']
return_sp500 = (SP500_today - SP500_past)/SP500_past

print(return_sp500)
#outcome
0.0218920970054796
We can therefore conclude that for the last 50 days, the S&P 500 passive strategy is outperforming Warren Buffett’s portfolio with a return of 2% vs the – 0.1% return obtained by Buffett’s holdings.

Wrapping Up
As we have seen in the last 50 days, the market has outperformed Berkshire Hathaway portfolio. In order to be able to draw better conclusions, I would encourage you to change the time frames and rerun the code. Is the market beating Warren Buffett if we take a longer time frame?

It may be worth exploring. However, to do the analysis right, it would require a full analysis for each of the changes on Buffettt’s portfolio and replicate the analysis quarter by quarter.