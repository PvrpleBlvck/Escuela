from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime 
import time

#cahnge url
url = "https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=4"
#url = 'https://www.sec.gov/edgar/searchedgar/companysearch.html'


page = requests.get(url)    
data = page.text
soup = BeautifulSoup(data, "lxml")
days_url = []
appended_dataframes = []

for link in soup.find_all('a'):
  if 'index' in link.get('href'):
    url_to_save = link.get('href')
    days_url.append(url_to_save)
for item in days_url:
  time.sleep(1)
  index ='https://www.sec.gov'+item

  index = pd.read_html(index)
  
  index = index[0]
  #change the type == 4
  index = index[(index['Document'].str.contains('.html')) & ( (index['Type'] == 4)| ( (index['Type'] == str(4)))) ]
  
  try:
    index = index['Document'].iloc[0]
  except:
    index = ''
  url = item.replace('-index.html','')
  url = url.replace('-','')
  url = 'https://www.sec.gov'+  url + '/xslF345X03/' + index
  url = url.replace('html','xml')
  cik_company = item.split('data/')[1].split('/')[0]
  print(url)
  try:
    insider_transactions = pd.read_html(url)
  except:
    insider_transactions = ''
    name = ''
  try:
    name = insider_transactions[3]
    name_person = name[0].iloc[0].split('*')[1].split('(')[0]
  except:
    name_person = ''
  try:
    ticker = name[1].iloc[0].split('[ ')[1].split(']')[0]
  except:
    ticker = ''
  try:
    position = name[2].iloc[0].split('(specify below)')[1]
  except:
    position = ''
  try:
    insider_transactions = insider_transactions[11]
    insider_transactions.reset_index(inplace=True)
    insider_transactions.columns = [['placeholder','Title','Date of Trans','Deemed Execution Day','Transaction Code','empty','Amount','Adq or Disp','Price','Shares Owned after Trans','Direct or Indirect Ownershipt','Nature of Ind Ownershipt']]
    insider_transactions['position'] = position
    insider_transactions['name_person'] = name_person
    insider_transactions['ticker'] = ticker
    appended_dataframes.append(insider_transactions)
  except:
    insider_transactions = ''
  
  print(name_person)
  print(position)
  time.sleep(2)
   
InsideTransactionsDF = pd.concat(appended_dataframes)