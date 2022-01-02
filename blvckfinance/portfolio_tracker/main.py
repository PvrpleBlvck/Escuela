import yfinance as yf
from notion.client import NotionClient
from datetime import datetime

client = NotionClient(token_v2="your token key")

cv = client.get_collection_view("https://www.notion.so/fadfdsf32321514?v=1223r234jhkhkh12")

tickers = ['AAPL','MSFT','VWRL.AS','CHF=X','AMZN','INTC']
for ticker in tickers:
  price = yf.Ticker(ticker)
  row = cv.collection.add_row()  
  
  hist = price.history(period="1d")
  row.Stock = ticker
  row.Date = datetime.today().strftime('%Y-%m-%d')
  row.Close = float(round((hist.Close[0]),1))
  row.Open = float(round((hist.Open[0]),1))
  row.Open = float(round((hist.Open[0]),1))
  row.Volume = float(round((hist.Volume[0]),1))
  row.High = float(round((hist.High[0]),1))
  row.DayReturn = float(round(((hist.Close[0]) - (hist.Open[0]) ) / (hist.Open[0])*100,2))