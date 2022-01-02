import requests
import os
api_key = os.getenv('api_key')

demo = api_key
stocks = ['AAPL','MSFT','GOOG']
for stock in stocks:
  income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={demo}').json()

  number_of_years = 0

  revenues = []
  operating_income = []
  net_income = []

  for item in income_statement:
    if number_of_years < 5:
      revenues.append(income_statement[number_of_years]['revenue'])
      operating_income.append(income_statement[number_of_years]['operatingIncome'])
      net_income.append(income_statement[number_of_years]['netIncome'])
      number_of_years += 1

  print(revenues)
 
  #import numpy to compute mean and std deviation
  import numpy
  revenues_array = numpy.array(revenues)
  operating_income_array = numpy.array(operating_income)
  net_income_array = numpy.array(net_income)


  CV_Sales = revenues_array.std() / revenues_array.mean()
  print('Revenue Coefficient of Variation for '+ stock + ' is ' + str(round(CV_Sales,2)))

  CV_OI = operating_income_array.std() / operating_income_array.mean()
  print('Operating Income Coefficient of Variation for '+ stock + ' is ' + str(round(CV_OI,2)))

  CV_Net_Income = net_income_array.std() / net_income_array.mean()
  print('Net Income Coefficient of Variation for '+ stock + ' is ' + str(round(CV_Net_Income,2)) +'\n')