import pandas as pd
import requests
import os
api_key = os.getenv('api_key')
demo = api_key

def cost_of_equity(stock):
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?apikey={demo}')
    IS = IS.json()
    dividend = IS['financials']
    Dtoday = float(dividend[0]['Dividend per Share'])


    #get dividend growht from previous 3 year dividends
    Div_2y = float(IS['financials'][1]['Dividend per Share'])
    Div_3y = float(IS['financials'][2]['Dividend per Share'])
    Div_4y = float(IS['financials'][3]['Dividend per Share'])
    dividend_growth = ( Div_2y - Div_4y)/Div_4y

    #price of the stock
    ccompany_info = requests.get(f"https://financialmodelingprep.com/api/v3/company/profile/{stock}?apikey={demo}")
    ccompany_info = ccompany_info.json()
    price =  float(ccompany_info['profile']['price'])

    #calculate cost of equity
    ke = (Dtoday*(1+dividend_growth)/price) + dividend_growth

    print(ke)

cost_of_equity('AAPL')


#what if we reduce the dividend growth
    dividend_growth = dividend_growth / 2

    ke_lower_growth = (Dtoday*(1+dividend_growth)/price) + dividend_growth
    print(ke_lower_growth)