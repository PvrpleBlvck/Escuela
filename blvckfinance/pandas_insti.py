from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime 
#1 Import the package
import sqlite3 as sql

import time

#2 Create SQL Connection
conn = sql.connect('form4.db')
url = "https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13F"

#3 Create the Cursor Object and the SCript to add a new Table SEC13F8 into the Database
try:
  c = conn.cursor()
  c.executescript('''
  CREATE TABLE SEC13F8 ("indice" TEXT PRIMARY KEY NOT NULL,
    "NAME OF ISSUER" TEXT,
    "TITLE OF CLASS" TEXT,
    "CUSIP" TEXT,
    "(x$1000)" TEXT,
    "PRN AMT" TEXT,
    "PRN" TEXT,
    "date_reported" DATE,
    "cik_company" TEXT
     );
                            ''')

  #close out the connection
  c.close()
#4 check that Table was created
  selection = pd.read_sql_query('''SELECT * FROM "SEC13F8"''',conn)
  print(selection)
except:
  print('table already exists')

#get all links
page = requests.get(url)    
data = page.text
soup = BeautifulSoup(data, "lxml")
days_url = []

days_url = days_url[0:2]

for link in soup.find_all('a'):
  if 'index' in link.get('href'):
    url_to_save = link.get('href')
    days_url.append(url_to_save)

for item in days_url:

  index ='https://www.sec.gov'+item
  index = pd.read_html(index)
  index = index[0]
  index = index[(index['Document'].str.contains('.html')) & (index['Type'].str.contains('INFORMATION TABLE'))]
  try:
    index = index['Document'].iloc[0]
  except:
    index = ''

  url = item.replace('-index.html','')
  url = url.replace('-','')
  url = 'https://www.sec.gov'+  url + '/xslForm13F_X01/' + index
  url = url.replace('html','xml')
  cik_company = item.split('data/')[1].split('/')[0]
  print(url)
  time.sleep(1)

  try:
    DF_13F = pd.read_html(url)
    DF_13F = DF_13F[-1]
    DF_13F = DF_13F.iloc[2:]
    new_header = DF_13F.iloc[0]
    DF_13F.columns = new_header
    DF_13F = DF_13F.iloc[1:]
    DF_13F['date_reported'] = datetime.now().strftime("%Y%m")
    DF_13F['cik_company'] = cik_company
    value_to_store_as_index = DF_13F['CUSIP']+cik_company + datetime.now().strftime("%Y%m")
    DF_13F['indice'] = value_to_store_as_index
    DF_13F = DF_13F[['indice','NAME OF ISSUER','TITLE OF CLASS','CUSIP','(x$1000)','PRN AMT','PRN','date_reported','cik_company']]
    print('new SEC13 report added to DataFrame')
    print(DF_13F)
    #5 Add the DF_13F containing the DataFrame into SQL table SEC13F8
    DF_13F.to_sql('SEC13F8',conn,if_exists='append',index=False)

  except:
    print('error')
    pass

#6 Select all record from the SEC13F8 table to be sure that the script worked as expected
selection = pd.read_sql_query('''SELECT * FROM "SEC13F8"''',conn)
print(selection)
