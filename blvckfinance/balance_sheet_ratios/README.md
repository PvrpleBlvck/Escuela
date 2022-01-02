# Activity Ratios
### Receivable Turnover. 
> The receivable turnover ratio indicates how many times a company collects its receivables over a period of time. Ideally, this ratio should be calculated using sales on credit. Unfortunately, sales on credit data is normally not made public by companies in their public reports. Therefore, we use revenue instead:

### Receivable Turnover = Revenue / Average receivables

### Day of Sales Outstanding (DSO). DSO represents the average number of days that it takes for a company to collect the outstanding receivables.

# DSO = Number of Days in period (e.g. 365) / Receivables Turnover


### Inventory Turnover. 
> The inventory turnover ratio represents the number of times that a company can turnover its inventory. That is, to sell and replace the inventory over a period.

## Inventory turnover = COGS / Average Inventory

### Days of Inventory on Hand (DOH). The DOH ratio indicates how many days the inventory remains in the company books before it is sold.

### DOH = Number of days in the period (e.g. 365) / Inventory Turnover

### Asset Turnover. The asset turnover ratio measures how efficient a company assets generate revenue.

# Asset Turnover = Revenue / Average Total Assets

### Liquidity Ratios
> Liquidity ratios help us to understand how capable a company is to meet its short term obligations.

### Current Ratio. 
> The current ratio is one of the main ratios to measure a firm’s liquidity. As a general norm, a higher ratio means that a company is more equipped to cover its current liabilities. However, having a too high current ratio may not be seen as a good sign since the company is probably not efficient enough managing its current assets. Too many current assets laying idle on the balance sheet instead of using them to add value for the shareholders.

### Current ratio = Current Assets / Current Liabilities

# Cash Ratio. 
> The cash ratio is another liquidity ratio. Cash ratio is much more stringent compared to the current ratio. The cash ratio only takes into account the two most liquid items within current assets, cash and short term marketable securities, to meet short term liabilities.

### Cash ratio = Cash + Short Term Marketable Securities / Current Liabilities


### Solvency Ratios
> We can use solvency ratios to assess how capable is a company to meet long term obligations.

### Long Term Debt or Debt to Equity. The higher this ratio, the more debt a company has in its capital structure.

# Debt to Equity = Total Debt (or LT Debt) / Total Equity

# Financial Leverage = Total Assets / Total equity

> As a note, you probably has realised that to calculate financial ratios where we have balance sheet data to income statement data, we use the average for the balance sheet account. The reason for it is the nature of balance sheet accounts which are moving over the year. We want to better capture the movement compare to simply taking the data in a single point of time.

> All financial ratios on a stand alone basis are not an indication of anything. We need to compare them across time or across firms to see if a company is improving the ratios over time or if it is doing better than its peers. For this kind of analysis, Python is our best friend.

### Balance Sheet Analysis with Python
> For our analysis, we will use Python in order to retrieve, process and prepare balance sheet data for our analysis. Since the code is very easy to build (assuming that you have followed my prior posts), I will simply share the code and provide a high level overview of what the code does. It will work as follows:

> Retrieve income statement data and balance sheet data from financialmodelingprep API. Remember to pass your API Key for the request to be successful.
Calculate all balance sheet related ratios.
Based on the user request, we will have an if-statement to determine if we want to have a cross sectional analysis vs time series analysis. For instance, if we pass only one ticker in the companies list, then the code will know that we want to have a time series analysis. On the contrary, if we pass more than one ticker within the list, we will get as a result a cross sectional balance sheet ratio analysis comparing different companies. Ideally, for this kind of analysis, it makes sense to select peer companies.
Finally, the results will be presented in the form of a Pandas DataFrame.
Balance sheet cross sectional analysis
If we want to get a balance sheet ratio comparison across companies, we simply need to pass a bunch of company tickers within the company lists. The list is included in the code line number four. As an example, below I have run the script for Apple, Amazon and Microsoft. Feel free to add as many companies as you want to the list.

