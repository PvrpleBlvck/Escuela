import pandas as pd
import requests
import time
from datetime import datetime
import os
api_key = os.getenv('api_key')


#Section A - Setting the variables and retrieving SP500 tickers
#api_key = 'your API KEY'
period_from ='2021-09-01'
period_to = '2021-11-30'

def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]

	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

companies_inSP500 = get_sp500()
companies_inSP500.insert(0,'^GSPC')


all_netincome = []
all_revenues = []
stock_to_buy = {}

#Section B - Checking for Condition number 1
for period in pd.date_range(period_from, period_to,freq = '1D'):
  #check if earnings are over next two days. For that, we first identify the range period between 2 days
  time.sleep(1)
  period1 = period
  period2 = period + pd.Timedelta('2D')
  url = f'https://financialmodelingprep.com/api/v3/earning_calendar?from={period1}&to={period2}&apikey={api_key}'
  earning_list = requests.get(url).json()
  #print(earning_list)
  #Get the stock ticker
  for stock in earning_list:
    stock = stock['symbol']
    duplication_ticker_check = []
    if stock in companies_inSP500:
      #print('it is part of SP500')
      #check for conditions

      #SECTION C - Checking for condition number 2
      #return on stock in the last 20 days more than 15%
      earning_range = period1 - pd.Timedelta('200D')
      to_per = period1.strftime("%Y-%m-%d")
      from_per = earning_range.strftime("%Y-%m-%d")
      #print(to_per,type(from_per)) #2018-03-12
      price = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={from_per}&to={to_per}&apikey={api_key}').json()
      
      try:
        if len(price['historical']) > 3:
          #create pd df
          return_stock = pd.DataFrame(price['historical'])
          #reverse the Dataframe to have most recent dates at the beginning
          return_stock = return_stock.iloc[::-1]
          return_stock['20d_return'] = (return_stock['adjClose'][0] - return_stock['adjClose'].shift(20))/return_stock['adjClose'].shift(20)
          #Condtion 2 - if return on stock in the last 20 days more than 15% - Very demanding feel free to relax to 5%
          if return_stock['20d_return'][0] > 0.15:
            print('Condition 1 and 2 are met')
            #if return more than 15%, we can test below condition number 3 on Moving Averages
            #Condition 3- moving average of volume over last 20 days more than moving average volume over last 60 days
            return_stock['volume_20d_MA'] = return_stock['adjClose'].rolling(window=20).mean()
            return_stock['volume_60d_MA'] = return_stock['adjClose'].rolling(window=60).mean()            
            if return_stock['volume_20d_MA'][0] >return_stock['volume_60d_MA'][0]:
              #print(return_stock)
              #SECTION D - Testing Condition number 4
              #Condition 4- revenue from the last reporting year > max revenue for the last three years
              url_rev = f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?limit=5&apikey={api_key}'
              revenue = requests.get(url_rev).json()
              all_revenues = []
              all_netincome = []
              print('Condition 3 is met')
              for item in revenue:
                all_revenues.append(item['revenue'])
                all_netincome.append(item['netIncome'])
              #Condtion 4 and 5 - revenues and net income are peaking compared to last years.
              #Note that we ignore element 0 if below is true. Since it refers tothe most recent reporting filing and that was unkown when the strategy occurs.
              #revenue[0]['filingDate'] shows the date of the most recent filing of the stock. If filing date is after the period in question, we will ignore it
              #comparison_period = revenue[0]['fillingDate'].strftime("%Y-%m-%d")
              comparison_period = revenue[0]['fillingDate']
              print(comparison_period, period1)
              if comparison_period > period1.strftime("%Y-%m-%d"):
                print('Ignore most recent filing since it is in the future vs when this strategy runs')
                if all_revenues[1] > all_revenues[2] and all_revenues[1] > all_revenues[3] and all_revenues[1] > all_revenues[4]:
                  #net income from the last reporting year > max net income for the last three years
                  #print(all_netincome[1] > all_netincome[2] and all_netincome[1] > all_netincome[3] and all_netincome[1] > all_netincome[4])
                  if all_netincome[1] > all_netincome[2] and all_netincome[1] > all_netincome[3] and all_netincome[1] > all_netincome[4]:
                    print('meets condition 4 and 5 as well stock:')
                    print(stock)
                    #print('continue net income')
                    #Section E - Condtion 6 and 7 on Quarterly revenue and net income.
                    #revenue last reporting quarter more than revenue for same quarter a year ago. Same for net income
                    #we ignore latest IS since reporting date is after the analysis is done
                    quarterlyIS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=6&apikey={api_key}').json()
                    #print(quarterlyIS[1])
                    revenue_lastqt = quarterlyIS[1]['revenue']
                    netincome_lastqt = quarterlyIS[1]['netIncome']
                    #print(quarterlyIS[5])
                    revenue_sameqtlastyear = quarterlyIS[5]['revenue']
                    netincome_sameqtlastyear = quarterlyIS[5]['netIncome']
                    #print(revenue_sameqtlastyear,revenue_lastqt)
                    #Condition 6 - Revenue last quarter 20% greater compared to same quarter last year
                    if revenue_lastqt > (revenue_sameqtlastyear*1.2):
                      print('we are good Condition 6 is also met by ')
                      print(stock)
                      #Condition 7 - Net Income last quarter 30% greater compared to same quarter last year
                      if netincome_lastqt > (netincome_sameqtlastyear*1.3):
                        print('all ok for entering position on')
                        print(stock)
                        if stock in duplication_ticker_check:
                          print('stock already exists in our selection. Ignoring this time')
                        else:
                          duplication_ticker_check.append(stock)
                          stock_to_buy[stock] = {}
                          stock_to_buy[stock]['date'] = period1
                          stock_to_buy[stock]['stock'] = stock
                          stock_to_buy[stock]['exit_date'] = period1+ pd.Timedelta('5D')
                          from_price_entry = stock_to_buy[stock]['date'].strftime("%Y-%m-%d")
                          to_price_exit = stock_to_buy[stock]['exit_date'].strftime("%Y-%m-%d")
                          time.sleep(1)
                          try:
                            price_entering_position = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={from_price_entry}&to={to_price_exit}&apikey={api_key}').json()
                            entering_price = price_entering_position['historical'][0]['adjClose']
                            exiting_price = price_entering_position['historical'][-1]['adjClose']
                            stock_to_buy[stock]['entering_price'] = entering_price 
                            stock_to_buy[stock]['exit_price'] = exiting_price
                            stock_to_buy[stock]['return_strategy'] = (exiting_price-entering_price)/entering_price
                            print('all okm stock has been added ',stock_to_buy)
                            
                          except:
                            print('problems retrieving stock prices for', stock)
              else: #here in case we want to use the most recent income statement filing(i.e. the filling date is before we run our trading strategy)
                print('we take most recent date')
                if all_revenues[0] > all_revenues[1] and all_revenues[0] > all_revenues[2] and all_revenues[0] > all_revenues[3]:
                  #net income from the last reporting year > max net income for the last three years
                  if all_netincome[0] > all_netincome[1] and all_netincome[0] > all_netincome[2] and all_netincome[0] > all_netincome[3]:
                    print(stock)
                    print('continue net income')
                    #Section E - Condtion 6 and 7 on Quarterly revenue and net income.
                    #revenue last reporting quarter more than revenue for same quarter a year ago. Same for net income
                    #we ignore latest IS since reporting date is after the analysis is done
                    quarterlyIS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=6&apikey={api_key}').json()
                    #print(quarterlyIS[1])
                    revenue_lastqt = quarterlyIS[1]['revenue']
                    netincome_lastqt = quarterlyIS[1]['netIncome']
                    #print(quarterlyIS[5])
                    revenue_sameqtlastyear = quarterlyIS[5]['revenue']
                    netincome_sameqtlastyear = quarterlyIS[5]['netIncome']
                    #print(revenue_sameqtlastyear,revenue_lastqt)
                    #Condition 6 - Revenue last quarter 20% greater compared to same quarter last year
                    if revenue_lastqt > (revenue_sameqtlastyear*1.2):
                      print('we are good')
                      #Condition 7 - Net Income last quarter 30% greater compared to same quarter last year
                      if netincome_lastqt > (netincome_sameqtlastyear*1.3):
                        print('all ok for entering position on' , stock)
                        if stock in duplication_ticker_check:
                          print('stock already exists in our selection. Ignoring this time')
                        else:
                          duplication_ticker_check.append(stock)
                          stock_to_buy[stock] = {}
                          stock_to_buy[stock]['date'] = period1
                          stock_to_buy[stock]['stock'] = stock
                          stock_to_buy[stock]['exit_date'] = period1+ pd.Timedelta('5D')
                          from_price_entry = stock_to_buy[stock]['date'].strftime("%Y-%m-%d")
                          to_price_exit = stock_to_buy[stock]['exit_date'].strftime("%Y-%m-%d")
                          time.sleep(1)
                          try:
                            price_entering_position = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={from_price_entry}&to={to_price_exit}&apikey={api_key}').json()
                            entering_price = price_entering_position['historical'][-1]['adjClose']
                            exiting_price = price_entering_position['historical'][0]['adjClose']
                            stock_to_buy[stock]['entering_price'] = entering_price 
                            stock_to_buy[stock]['exit_price'] = exiting_price
                            stock_to_buy[stock]['return_strategy'] = (exiting_price-entering_price)/entering_price
                            print('all ok ',stock_to_buy)
                            
                          except:
                            print('problems retrieving stock prices for', stock)    
      except:
        print('no data in API for this stock')
        continue
  time.sleep(1)
  print('next day',period1)

#Section F
total_return = []
for stock in stock_to_buy:
  print(stock)
  try:
    total_return.append(stock_to_buy[stock]['return_strategy'])
    print('ok')
  except:
    print('error')

SP500 = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/^GSPC?from={period_from}&to={period_to}&apikey={api_key}').json()
SP500_entry = SP500['historical'][-1]['adjClose']
SP500_exit = SP500['historical'][0]['adjClose']
SP500_return = (SP500_exit-SP500_entry)/SP500_entry
print('our strategy return',sum(total_return))
print('vs the SP 500 return of during the same period', SP500_return)

print(pd.DataFrame(stock_to_buy))