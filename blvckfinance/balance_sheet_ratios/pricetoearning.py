import pandas as pd

import requests
import os
api_key = os.getenv('fmpapi_key')
demo = api_key

PtoE= {}
    
querytickers = requests.get(f'https://fmpcloud.io/api/v3/search?query=&exchange=NASDAQ&limit=5000&apikey={demo}')
querytickers = querytickers.json()

list_500 = querytickers

def getPricetoEarnings(stock):
    IS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}&apikey={demo}'")
    IS = IS.json()
    earnings = float(IS['financials'][0]['Net Income'])  

    company_info = requests.get(f"https://financialmodelingprep.com/api/v3/company/profile/{stock}&apikey={demo}'")
    company_info = company_info.json()
    market_cap =  float(company_info['profile']['mktCap'])
    
    PtoEarnings = market_cap/earnings
    PtoE[stock] = PtoEarnings
    return PtoE

stocks = []
count = 0
for item in list_500:
    count = count +1
    #Stop after storing 500 stocks
    if count < 50:
        stocks.append(item['symbol'])
        
for item in stocks:
    profile = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{item}&apikey={demo}'')
    profile = profile.json()
    try:
        sector = profile['profile']['sector']
        #marketcap in millions
        mktcap = profile['profile']['mktCap']
        mktcap = float(mktcap)/1000
        if ((sector == 'Technology') & (10000 <= mktcap <= 100000)):
            try:
                getPricetoEarnings(item)
            except:
                pass
    except:
        pass
        

PtoE