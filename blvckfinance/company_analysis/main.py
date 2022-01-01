import requests 
import pandas as pd
import xlsxwriter 
import plotly.graph_objects as go
import numpy as np 
from textblob import TextBlob
import numpy as np
import requests
import pandas as pd
import nltk
import webbrowser

import os
api_key = os.getenv('api_key')

def income_statement_growth(stock):

  url = f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=35&apikey={api_key}'
  writer = pd.ExcelWriter('MyFile.xlsx', engine='xlsxwriter')
  IS = requests.get(url).json()
  pd.options.display.precision = 2
  income_statement = {}
  for item in IS:
    income_statement[item['date']] = {}
    income_statement[item['date']]['Revenue'] = item['revenue']
    income_statement[item['date']]['COGS'] = item['costOfRevenue']
    income_statement[item['date']]['Gross Profit'] = item['grossProfit']
    income_statement[item['date']]['R&D'] = item['researchAndDevelopmentExpenses']
    income_statement[item['date']]['G&A'] = item['generalAndAdministrativeExpenses']
    income_statement[item['date']]['M&S'] = item['sellingAndMarketingExpenses']
    income_statement[item['date']]['other Expenses'] = item['otherExpenses']
    income_statement[item['date']]['opearting Expenses'] = item['operatingExpenses']
    income_statement[item['date']]['operating Income'] = item['operatingIncome']
    income_statement[item['date']]['Income Before Tax'] = item['incomeBeforeTax']
    income_statement[item['date']]['Income Tax Expense'] = item['incomeTaxExpense']
    income_statement[item['date']]['Net Income'] = item['netIncome']
    income_statement[item['date']]['EPS'] = item['eps']


  Income_statement_DF = pd.DataFrame(income_statement) / 1000000
  Income_statement_actual = pd.DataFrame(income_statement) / 1000000
  

  def percentage_change(col1,col2):
      return ((col2 - col1) / col1) * 100
  for item in range(len(Income_statement_DF.columns)):
    item = int(item)
    prior_year_same_quarter = item + 4
    try:
      #show IS as percentage change
      Income_statement_DF[Income_statement_DF.columns[item]] = percentage_change(Income_statement_DF.iloc[:,prior_year_same_quarter],Income_statement_DF.iloc[:,item])
    except:
      print('last one')


  Income_statement_DF.to_excel(writer, sheet_name = 'IS Perc Growth')
  Income_statement_actual.to_excel(writer, sheet_name = 'IS Last X Yrs')
  
  print(Income_statement_DF)
  return Income_statement_actual, writer, Income_statement_DF

def plot_income_statement(stock,Income_statement_actual,writer,Income_statement_DF):
  Income_statement_dates = Income_statement_actual.columns.to_list()
  fig = go.Figure()
  fig.add_trace(go.Bar(
      x=Income_statement_actual.columns.to_list(),
      y=Income_statement_actual.iloc[0,:].to_list(),
      name='Revenue',
      marker_color='indianred'
  ))
  fig.add_trace(go.Bar(
      x=Income_statement_actual.columns.to_list(),
      y=Income_statement_actual.iloc[11,:].to_list(),
      name='Net Income',
      marker_color='lightsalmon'
  ))

  fig.update_layout(barmode='group', xaxis_tickangle=-45)
  #fig.show()

  #install to work pip install -U kaleido PLOTLY 4.9 or higher version required!!!!
  fig.write_image("fig_plotly.png")
  #save picture to Excel
  worksheet = writer.sheets['IS Last X Yrs']
# Insert an image.
  worksheet.insert_image('A21', 'fig_plotly.png')

  #Income Growth PLOT
  Income_statement_DF_T = Income_statement_DF.T
  Income_statement_DF_T = Income_statement_DF_T[:-5]
  Income_statement_DF_T["Color"] = np.where(Income_statement_DF_T["Revenue"]<0, 'red', 'green')
  fig = go.Figure()
  fig.add_trace(
      go.Bar(name='Net',
            x=Income_statement_DF_T.index,
            y=Income_statement_DF_T['Revenue'],
            marker_color=Income_statement_DF_T['Color']))
  fig.update_layout(barmode='stack')
  #fig.show()
  fig.write_image("fig2_plotly.png")
  worksheet = writer.sheets['IS Perc Growth']
  worksheet.insert_image('A21', 'fig2_plotly.png')


def peers(stock):
  url = f'https://financialmodelingprep.com/api/v4/stock_peers?symbol={stock}&apikey={api_key}'

  #1 GET LIST OF PEERS
  peers = requests.get(url).json()
  peers = peers[0]['peersList']
  peers.append(stock)
  profitability_ratios = {}
  #2 Retrieve Profitability Ratios for each of the peers
  for stock in peers:
    #3 Add to Python Dictionary
    profitability_ratios[stock] = {}
    fr = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{stock}?apikey={api_key}'
    financial_ratios_ttm = requests.get(fr).json()
    profitability_ratios[stock]['Return on Assets'] = financial_ratios_ttm[0]['returnOnAssetsTTM']
    profitability_ratios[stock]['Return on Equity'] = financial_ratios_ttm[0]['returnOnEquityTTM']
    profitability_ratios[stock]['Gross Profit Margin'] = financial_ratios_ttm[0]['grossProfitMarginTTM']
    profitability_ratios[stock]['Opearting Profit Margin'] = financial_ratios_ttm[0]['operatingProfitMarginTTM']
    profitability_ratios[stock]['Net Profit Margin'] = financial_ratios_ttm[0]['netProfitMarginTTM']

  #4 Convert into Pandas DataFrame
  profitability_ratios = pd.DataFrame(profitability_ratios)
  profitability_ratios['mean'] = profitability_ratios.mean(axis=1)
  profitability_ratios.to_excel(writer, sheet_name = 'profitability_ratios')
  

  import plotly.graph_objects as go

  fig = go.Figure()
  fig.add_trace(go.Bar(
      x=profitability_ratios.T.index,
      y=profitability_ratios.T['Return on Assets'],
      name='Return on Assets',
      marker_color='indianred'
  ))
  fig.add_trace(go.Bar(
      x=profitability_ratios.T.index,
      y=profitability_ratios.T['Return on Equity'],
      name='Return on Equity',
      marker_color='blue'
  ))

  fig.add_trace(go.Bar(
      x=profitability_ratios.T.index,
      y=profitability_ratios.T['Net Profit Margin'],
      name='Net Profit Margin',
      marker_color='green'
  ))

  fig.add_trace(go.Bar(
      x=profitability_ratios.T.index,
      y=profitability_ratios.T['Opearting Profit Margin'],
      name='Op Profit Margin',
      marker_color='purple'
  ))

  fig.add_trace(go.Bar(
      x=profitability_ratios.T.index,
      y=profitability_ratios.T['Gross Profit Margin'],
      name='Gross Profit Margin',
      marker_color='orange'
  ))

  fig.update_layout(barmode='group', xaxis_tickangle=-45)
  #fig.show()
  fig.write_image("fig3_plotly.png")
  worksheet = writer.sheets['profitability_ratios']
  worksheet.insert_image('A21', 'fig3_plotly.png')
  return peers


def institutional_investors(stock,peer):
  companies = peer
  change = {}

  for company in companies:
    institutions = requests.get(f'https://financialmodelingprep.com/api/v3/institutional-holder/{company}?apikey={api_key}').json()
    change[company] = {}
    identify = 0
    count_down = 0
    count_up = 0
    total_shares_exchanged = 0
    for item in institutions:
      identify = identify + 1
      if item['dateReported'] > '2022-02-11':
        change[company][item['dateReported']+ str(identify)] = item['change']
        if item['change'] > 0:
          count_up = count_up + 1
        if item['change'] < 0:
          count_down = count_down + 1
        total_shares_exchanged = total_shares_exchanged + item['change']

    change[company]['total'] = count_up + count_down
    change[company]['buys'] = count_up
    change[company]['sells'] = count_down
    change[company]['total_shares_exchanged'] = total_shares_exchanged

  institutions_DF = pd.DataFrame(change)
  institutions_DF = institutions_DF.T 

  institutions_DF = institutions_DF[['total','buys','sells','total_shares_exchanged']]
  institutions_DF.to_excel(writer, sheet_name = 'institutional_investors')
  print(institutions_DF)


def earning_surprises(stock):
  earning_surprises = f'https://financialmodelingprep.com/api/v3/earnings-surprises/{stock}?apikey={api_key}'

  earning_surprises = requests.get(earning_surprises).json()
  earning_surprises = pd.DataFrame(earning_surprises)
  earning_surprises['miss_beat_by'] = (earning_surprises['actualEarningResult'] - earning_surprises['estimatedEarning'])/earning_surprises['estimatedEarning']
  earning_surprises.to_excel(writer, sheet_name = 'earning_surprise')

  fig = go.Figure(data=[
      go.Bar(name='Actual Earnings', x=earning_surprises.date, y=earning_surprises.actualEarningResult),
      go.Bar(name='Estimated Earnings', x=earning_surprises.date, y=earning_surprises.estimatedEarning),
      go.Bar(name='beat_by/miss by in %', x=earning_surprises.date, y=earning_surprises.miss_beat_by)
  ])
  # Change the bar mode
  fig.update_layout(barmode='group')
  #fig.show()
  fig.write_image("fig4_plotly.png")
  worksheet = writer.sheets['earning_surprise']
  worksheet.insert_image('A15', 'fig4_plotly.png')

def earning_transcript_sentiment(stock,quarter,year):
  #pip3 install textblob
  nltk.download('punkt')
  transcript = requests.get(f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{stock}?quarter={quarter}&year={year}&apikey={api_key}').json()

  transcript = transcript[0]['content']
  sentiment_call = TextBlob(transcript)
  print(sentiment_call.sentiment)
  sentiment_call.sentences
  negative = 0
  positive = 0
  neutral = 0
  all_sentences = []

  for sentence in sentiment_call.sentences:
    #print(sentence.sentiment.polarity)
    if sentence.sentiment.polarity < 0:
      negative +=1
    if sentence.sentiment.polarity > 0:
      positive += 1
    else:
      neutral += 1
  
    all_sentences.append(sentence.sentiment.polarity) 

  print('positive: ' +  str(positive))
  print('negative: ' +  str(negative))
  print('neutral: ' + str(neutral))

  all_sentences = np.array(all_sentences)
  print('sentence polarity: ' + str(all_sentences.mean()))

  #very positive sentences
  for sentence in sentiment_call.sentences:
    if sentence.sentiment.polarity > 0.8:
      print(sentence)

  print('very negative sentences')
  for sentence in sentiment_call.sentences:
    if sentence.sentiment.polarity < -0.2:
      print(sentence)


def earning_transcript_analysis(stock,quarter,year):
  word_to_analyze = 'expect'
  transcript = requests.get(f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{stock}?quarter={quarter}&year={year}&apikey={api_key}').json()
  transcript = transcript[0]['content'].split('\n')
  earnings_call = pd.DataFrame(transcript,columns=['content'])

  analysis = earnings_call[earnings_call['content'].str.contains(word_to_analyze)]
  text_earnings = analysis['content'].values


  for text in text_earnings:
    for phrase in text.split('. '):
      if word_to_analyze in phrase:
        print(phrase)
        print()

def price_ratios(peer):
  pd.options.display.float_format = '{:,.2f}'.format

  stocks = peer #peer
  metrics = {}
  for stock in stocks:
    metrics[stock] = {}
    url = f'https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={api_key}'

    quote = requests.get(url).json()

    

    metrics[stock]['Price'] = quote[0]['price']
    metrics[stock]['Market Cap'] = quote[0]['marketCap']
    metrics[stock]['Year High']= quote[0]['yearHigh']
    metrics[stock]['Year Low']= quote[0]['yearLow']

    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=4&apikey={api_key}').json()
    BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&limit=4&apikey={api_key}').json()
    revenue = []
    earnings = []
    book_value = []
    #we need the trailing 12 months. So we take last 4 quarters
    for item in IS:
      #print(item)
      revenue.append(item['revenue'])
      earnings.append(item['netIncome'])
      
    for item in BS:
      #print(item)
      book_value.append(item['totalStockholdersEquity'])

    metrics[stock]['revenue_TTM'] = round(sum(revenue),1)
    metrics[stock]['earnings_TTM'] = round(sum(earnings),1)
    metrics[stock]['average_book_value'] = round(sum(book_value) / 4,0)

    metrics[stock]['PE_TTM'] = round(metrics[stock]['Market Cap'] / metrics[stock]['earnings_TTM'],1)
    metrics[stock]['PS_TTM'] = round(metrics[stock]['Market Cap'] / metrics[stock]['revenue_TTM'],1)
    metrics[stock]['PB'] = round(metrics[stock]['Market Cap'] / metrics[stock]['average_book_value'],1)

    

  price_ratios = pd.DataFrame(metrics)
  price_ratios['mean'] = price_ratios.mean(axis=1)
  print(price_ratios)
  price_ratios.to_excel(writer, sheet_name = 'price_ratios')


def trading_view_charts(stock):
	url =  f'https://www.tradingview.com/symbols/{stock}/'
	webbrowser.open(url, new=1, autoraise=True)
	print('check the browser')
	

def trading_news(stock):
  news = requests.get(f'https://financialmodelingprep.com/api/v3/stock_news?tickers={stock}&limit=50&apikey={api_key}').json()

  news_all = {}
  for item in news:
    date = item['publishedDate']
    news_all[date] = {}
    news_all[date]['title'] = item['title']
    news_all[date]['source'] = item['site']
    news_all[date]['url'] = item['url']
    news_all[date]['text'] = item['text']

  news_DF = pd.DataFrame(news_all).T
  news_DF.to_excel(writer, sheet_name = 'latest_news')

quarter = input('quarter for earning transcript? E.g. 2: ').strip()
year = input('year for earning transcript? E.g. 2021: ').strip()
stock = input('company ticker? e.g AAPL: ').strip()


Income_statement_actual,writer,Income_statement_DF = income_statement_growth(stock)
plot_income_statement(stock,Income_statement_actual,writer,Income_statement_DF)
peer = peers(stock)
institutional_investors(stock,peer)
earning_surprises(stock)
earning_transcript_sentiment(stock,quarter,year)
earning_transcript_analysis(stock,quarter,year)
price_ratios(peer)
trading_view_charts(stock)
trading_news(stock)

writer.save()