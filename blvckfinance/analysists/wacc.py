#cost of equity
import pandas_datareader.data as web
import datetime
import requests
import os
api_key = os.getenv('api_key')


company = 'MSFT'
demo = api_key
#Interest coverage ratio = EBIT / interest expenses

def interest_coveraga_and_RF(company):
  IS= requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey={demo}').json()
  EBIT= IS[0]['ebitda'] - IS[0]['depreciationAndAmortization'] 
  interest_expense = IS[0]['interestExpense']
  interest_coverage_ratio = EBIT / interest_expense

    #RF
  start = datetime.datetime(2019, 7, 10)
        
  end= datetime.datetime.today().strftime('%Y-%m-%d')
  #end = datetime.datetime(2020, 7, 10)

  Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
  RF = float(Treasury.iloc[-1])
  RF = RF/100
  print(RF,interest_coverage_ratio)
  return [RF,interest_coverage_ratio]
  

#Cost of debt
def cost_of_debt(company, RF,interest_coverage_ratio):
  if interest_coverage_ratio > 8.5:
    #Rating is AAA
    credit_spread = 0.0063
  if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
    #Rating is AA
    credit_spread = 0.0078
  if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
    #Rating is A+
    credit_spread = 0.0098
  if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
    #Rating is A
    credit_spread = 0.0108
  if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
    #Rating is A-
    credit_spread = 0.0122
  if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
    #Rating is BBB
    credit_spread = 0.0156
  if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
    #Rating is BB+
    credit_spread = 0.02
  if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
    #Rating is BB
    credit_spread = 0.0240
  if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
    #Rating is B+
    credit_spread = 0.0351
  if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
    #Rating is B
    credit_spread = 0.0421
  if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
    #Rating is B-
    credit_spread = 0.0515
  if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
    #Rating is CCC
    credit_spread = 0.0820
  if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
    #Rating is CC
    credit_spread = 0.0864
  if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
    #Rating is C
    credit_spread = 0.1134
  if interest_coverage_ratio <=  0.2:
    #Rating is D
    credit_spread = 0.1512
  
  cost_of_debt = RF + credit_spread
  print(cost_of_debt)
  return cost_of_debt


def costofequity(company):


  #RF
  start = datetime.datetime(2019, 7, 10)
  end= datetime.datetime.today().strftime('%Y-%m-%d')
  #end = datetime.datetime(2020, 7, 10)

  Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
  RF = float(Treasury.iloc[-1])
  RF = RF/100

#Beta

  beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={demo}')
  beta = beta.json()
  beta = float(beta['profile']['beta'])


  #Market Return
  start = datetime.datetime(2019, 7, 10)
  end= datetime.datetime.today().strftime('%Y-%m-%d')

  SP500 = web.DataReader(['sp500'], 'fred', start, end)
      #Drop all Not a number values using drop method.
  SP500.dropna(inplace = True)

  SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
    
  cost_of_equity = RF+(beta*(SP500yearlyreturn - RF))
  print(cost_of_equity)
  return cost_of_equity

#effective tax rate and capital structure
def wacc(company):
  FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()

  ETR = FR[0]['effectiveTaxRate']

# 
  BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&apikey={demo}').json()



  Debt_to = BS[0]['totalDebt'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
  equity_to = BS[0]['totalStockholdersEquity'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])

  WACC = (kd*(1-ETR)*Debt_to) + (ke*equity_to)
  print(WACC,equity_to,Debt_to)
  return WACC

company = 'MSFT'
demo = 'your api key'

RF_and_IntCov = interest_coveraga_and_RF(company)
RF = RF_and_IntCov[0]
interest_coverage_ratio = RF_and_IntCov[1]
ke = costofequity(company)
kd = cost_of_debt(company,RF,interest_coverage_ratio)
wacc_company = wacc(company)
print('wacc of ' + company + ' is ' + str((wacc_company*100))+'%')