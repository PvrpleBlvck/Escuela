import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json

def selectquote(quote):
     r= requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{quote}?period=quarter")
     r = r.json()
    stock = r['financials']
    stock = pd.DataFrame.from_dict(stock)
    stock = stock.T
    stock.columns = stock.iloc[0]
    stock.reset_index(inplace=True)
    stock = stock.iloc[:,0:2]
    stock.rename(columns={ stock.columns[1]: quote }, inplace = True)
    cols = stock.columns.drop('index')
    stock[cols] = stock[cols].apply(pd.to_numeric, errors='coerce')
    stock = stock.iloc[1:,]
    return stock

incomeStatement = selectquote('AAPL')
Revenue = incomeStatement[incomeStatement['index'] == 'Revenue'].iloc[0][1]
COGS = incomeStatement[incomeStatement['index'] == 'Cost of Revenue'].iloc[0][1]*-1
grossProfit = incomeStatement[incomeStatement['index'] == 'Gross Profit'].iloc[0][1] 
RD = incomeStatement[incomeStatement['index'] == 'R&D Expenses'].iloc[0][1]-1 
GA = incomeStatement[incomeStatement['index'] == 'SG&A Expense'].iloc[0][1]-1
operatingExpenses = incomeStatement[incomeStatement['index'] == 'Operating Expenses'].iloc[0][1]-1 
interest = incomeStatement[incomeStatement['index'] == 'Interest Expense'].iloc[0][1]-1
EBT = incomeStatement[incomeStatement['index'] == 'Earnings before Tax'].iloc[0][1]
incTax = incomeStatement[incomeStatement['index'] == 'Income Tax Expense'].iloc[0][1]*-1
netIncome = incomeStatement[incomeStatement['index'] == 'Net Income'].iloc[0][1] 

fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["relative", "relative", "total", "relative", "relative", "total","relative","total","relative","total"],

    x = ["Revenue", "COGS", "Gross Profit", "RD", "G&A", "Operating Expenses","Interest Expense", "Earn Before Tax","Income Tax","Net Income"],
    textposition = "outside",

    text = [Revenue/100000, COGS/100000, grossProfit/100000, RD/100000, GA/1000000, operatingExpenses/1000000,interest/100000, EBT/100000,incTax/100000, netIncome/100000],

     y = [Revenue, COGS, grossProfit, RD, GA, operatingExpenses, interest,EBT,incTax,netIncome],

    connector = {"line":{"color":"rgb(63, 63, 63)"}},
     
fig.update_layout(
         title = "Profit and loss statement",
         showlegend = True
 )))

fig.show()