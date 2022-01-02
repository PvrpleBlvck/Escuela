Mark Minervini shares a few key elements in order to spot super performer stocks:

Stock prices should be having an upward trend.
Strong fundamentals. Super performance stocks are constantly beating revenues and earnings.
Stock has a catalyst that will push the price up. E.g. New CEO or a new and impactful product.
Find the entry points at which to buy the stock. Price graphs are great for this purpose.
Know when to exit and limit your risks. Stop Losses are essential.
In this post, we will build a screener to identify stocks having a long upward trend as per Mark’s approach.

Stocks meeting this criteria are the ones that Mark Minervini considers as having the best change to become the next superperformers.

Searching for Super Performance Stocks with Python
Photo by Gabby K on Pexels.com
Screening to Identify Super Performance Stocks
In order to find stocks with a long term upward trend, Mark Minervini provides what he calls a trend template, that is a set of rules that a stock needs to fulfil in order to have chances of becoming a true superperformer stock.

Normally, superperformers are small or mid-cap companies. But from time to time big companies may also be included.

I will list the rules below and in the next section, we will build the Python script in order to build the screener to find stocks meeting his criteria.

For a stock to qualify as a Potential candidate all rules below need to be met:

Current stock price is above the 150 and 200 days moving average (MA).
The 150 days moving average is above the 200 days moving average.
The 200 days moving average is trending up for at least a month.
The 50 day MA is above the 150 and 200 MAs
Stock price is above the 50 day MA
Current share price is at least 30% above its 52 week low
Current stock price is at least within 25% of the 52 week high
Relative Strength ranking (i.e. how good stock performed against market) is greater than 80 or 90
If a stock meets all eight criteria points, we have found a stock that is in a clear uptrend phase.

Finding Superperfomer Stock Candidates with Python
Now that we understand how to indentify stocks in an upward trend as per Mark Minervini trend template, we can build a Python script to do the work for us.

We will perform the screener using all stocks in the S&P 500 index. I will not go into much details on how the code works since it is quite long and the majority of the steps are similar to the ones covered in my previous posts on Python for Finance:

First, we start by getting a list of all tickers in the S&P500. This is our starting point. We can get them by scraping Wikipedia. The result of this be a Python list containing all S&P500 tickers. We insert the SP500 index as well to be the first element of that list:

def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]

	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

companies = get_sp500()
companies.insert(0,'^GSPC')

The reason why need to have the tickers in a Python list is to be able to loop through them to retrieve historical prices with Python. With the stock historical prices, we will be able to calculate all financial metrics required to test the eight conditions of the trend template.

We will use financialmodelingprep in order to retrieve stock prices. Note that an API key is required in order to be able to get the historical prices from the 500 stocks.

We will first loop through each of the stocks and retrieve the data and the stock price for each of the days. That will be added to a dictionary called price.

Next, we convert the dictionary into a Pandas DataFrame. That will let us calculate the required metrics for each of the stocks such as moving average, relative strength, etc. All these metrics are based on the stock prices.

The only metric that is first time introduced in this blog is the relative strength. It tells us how the stock has performed compared to an index (i.e. S&P500). In our case, we calculate the relative strength of each stock respect to the S&P500. Feel free to read more about how to calculat relative strength on the following link.

Note that we calculate and store in a dictionary called metrics all moving averages and other financial metrics required for the test.

Finally, we convert the metrics dictionary into a Pandas DataFrame that we save into a csv file.

The code may seems a bit complicated. Since the script is a bit long, it is not easy to explain line by line in a blog post. I have recorded below video explaining each of the steps in the code. That way you should be able to follow the script logic without any troubles.