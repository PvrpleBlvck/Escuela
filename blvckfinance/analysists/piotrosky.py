import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime as dt
import re
from sklearn.linear_model import LinearRegression

tickers = ["HON", "GE", "ITW", "MMM", "ROP",  "EMR", "ETN", "CMI", "ROK", "PH"]
F_score_2018 = [ ]
F_score = pd.DataFrame(index=tickers)


for ticker in tickers:
    #Balance Sheet
    print(f"Analyzing {ticker}")
    bs = requests.get(f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?period=quarter")
    bs = bs.json()
    if re.search('2018-1\d-\d\d', bs["financials"][3]['date']):
        a,b,c = 3,7,11
    elif re.search('2018-1\d-\d\d', bs["financials"][5]['date']):
        a,b,c = 5,9,13
    elif re.search('2018-1\d-\d\d', bs["financials"][4]['date']):
        a,b,c = 4,8,12
    else:
        print(f"No match for desired date in {ticker}")
        a,b,c = 6,10,14
    
    print("year of study is "+bs["financials"][a]['date'])
    #Year 2018
    long_term_debt = float(bs["financials"][a]['Long-term debt'])
    total_assets = float(bs["financials"][a]['Total assets'])
    current_assets = float(bs["financials"][a]['Total current assets'])
    current_liabilities = float(bs["financials"][a]['Total current liabilities'])
    
    #Previous year (2017)
    long_term_debt_py = float(bs["financials"][b]['Long-term debt'])
    total_assets_py = float(bs["financials"][b]['Total assets'])
    current_assets_py = float(bs["financials"][b]['Total current assets'])
    current_liabilities_py = float(bs["financials"][b]['Total current liabilities'])
    #Previous year*2 (2016)
    total_assets_py2 = float(bs["financials"][c]['Total assets'])
    
    # Income statement
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?period=quarter')
    IS = IS.json()
    # Year 2018
    revenue = float(IS['financials'][a]['Revenue'])+float(IS['financials'][a+1]['Revenue'])+float(IS['financials'][a+2]['Revenue'])+float(IS['financials'][a+3]['Revenue'])
    gross_profit = float(IS['financials'][a]['Gross Profit'])+float(IS['financials'][a+1]['Gross Profit'])+float(IS['financials'][a+2]['Gross Profit'])+float(IS['financials'][a+3]['Gross Profit'])
    net_income = float(IS['financials'][a]['Net Income'])+float(IS['financials'][a+1]['Net Income'])+float(IS['financials'][a+2]['Net Income'])+float(IS['financials'][a+3]['Net Income'])
    #Previous year (2017)
    revenue_py = float(IS['financials'][b]['Revenue'])+float(IS['financials'][b+1]['Revenue'])+float(IS['financials'][b+2]['Revenue'])+float(IS['financials'][b+3]['Revenue'])
    gross_profit_py = float(IS['financials'][b]['Gross Profit'])+float(IS['financials'][b+1]['Gross Profit'])+float(IS['financials'][b+2]['Gross Profit'])+float(IS['financials'][b+3]['Gross Profit'])
    net_income_py = float(IS['financials'][b]['Net Income'])+float(IS['financials'][b+1]['Net Income'])+float(IS['financials'][b+2]['Net Income'])+float(IS['financials'][b+3]['Net Income'])
    
    #Cashflow
    CF = requests.get(f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?period=quarter')
    CF = CF.json()
    cashflow_op = float(CF['financials'][a]["Operating Cash Flow"])+float(CF['financials'][a+1]["Operating Cash Flow"])+float(CF['financials'][a+2]["Operating Cash Flow"])+float(CF['financials'][a+3]["Operating Cash Flow"])
    
    #Piotroski F-score
    ROA_FS = int(net_income/((total_assets + total_assets_py)/2)>0)
    CFO_FS = int(cashflow_op>0)
    ROA_D_FS = int((net_income/((total_assets + total_assets_py)/2))>(net_income_py/((total_assets_py + total_assets_py2))))
    CFO_ROA_FS = int((cashflow_op/total_assets)>(net_income/((total_assets + total_assets_py)/2)))
    LTD_FS = int(long_term_debt <= long_term_debt_py)
    CR_FS = int((current_assets/current_liabilities)>(current_assets_py/current_liabilities_py))
    DILUTION_FS = int(float(IS['financials'][a]['Weighted Average Shs Out'])<=float(IS['financials'][b]['Weighted Average Shs Out']))
    GM_FS = int(gross_profit/revenue>gross_profit_py/revenue_py)
    ATO_FS = int((revenue/((total_assets + total_assets_py)/2))>(revenue_py/((total_assets_py + total_assets_py2))))
    f_sc = ROA_FS + CFO_FS + ROA_D_FS + CFO_ROA_FS + LTD_FS + CR_FS + DILUTION_FS + GM_FS + ATO_FS     
    print(f'{ticker} f score is {f_sc}')
    F_score_2018.append(f_sc)


F_score["F_score"] = F_score_2018


# PRICE & DIVIDENDS

def return_with_divs(tickers):
    rend2 = []
    for ticker in tickers:
        data = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line')
        data = data.json()
        
        Date = []
        Price = []
        years = 2
        for i in range(1, (252*years+1)):
            Date.append(dt.datetime.strptime(data["historical"][-i]["date"],"%Y-%m-%d"))
            Price.append(float(data["historical"][-i]["close"]))
        
        stock = pd.DataFrame()
        stock["Date"] = Date[::-1]
        stock["Price"] = Price[::-1]
        stock.set_index("Date", inplace=True)
        
        div = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ticker}')
        div = div.json()
        Date = []
        Dividend = []
        years = 2
        margin = 6
        for i in range(4*years+margin):
            Date.append(dt.datetime.strptime(div["historical"][i]["date"],"%Y-%m-%d"))
            Dividend.append(float(div["historical"][i]["adjDividend"]))
        
        dividends = pd.DataFrame()
        dividends['Date'] = Date[::-1]
        dividends['Dividend'] = Dividend[::-1]
        dividends.set_index("Date", inplace=True)
        
        total = pd.merge(left=stock, right=dividends, how="left", left_on="Date", right_on="Date")
        
        total["var"] = total["Price"].pct_change()
        total.fillna(0, inplace=True)
        
        adj_price = [total["Price"][0]]
        
        for i in range(1, len(total)):      
                adj_price.append(total["Dividend"][i] + (adj_price[i-1]*(1+total["var"][i])))
        total["adj_price"] = adj_price
        for i in range(len(total)):
            if total["Dividend"][i] != 0:
                print(ticker,": dividend of", total["Dividend"][i], "on date:", total.index[i])
        total = total.resample('Y').last()
        
        variation = round(total["adj_price"][-1] / total["adj_price"][0] -1, 2)
        rend2.append(variation)
        print(f'{ticker} variation+dividends was {round(variation*100,2)}%')
    return rend2


# REGRESSION
x_pred = F_score[["F_score"]]
y= F_score[["return+div"]]
lm = LinearRegression()
lm.fit(x_pred, y)
r2 = lm.score(x_pred,y)
F_score["y_pred"] = lm.intercept_ + lm.coef_ * F_score[["F_score"]]
print(f"Linear regression has a R-squared of {r2}")


# GRAPH

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [10,6]

plt.scatter(F_score["F_score"], F_score["return+div"], color="red")
plt.plot(F_score["F_score"], F_score["y_pred"], color="black", lw=0.75)
plt.title(tickers)
plt.xlabel("F-Score end-2018", color="black")
plt.ylabel("Posterior return", color="black")
plt.text(7.5,F_score["return+div"].mean(),f"R2={round(r2,2)}")
plt.show()

