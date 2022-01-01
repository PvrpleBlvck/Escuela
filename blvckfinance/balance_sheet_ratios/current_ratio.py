import requests
import pandas as pd 

companies = ['AAPL','GOOGL','FB','MSFT']

Current_ratio_dictionary = {}

for company in companies:
  Current_ratio_dictionary[company] = {}
  BS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{company}').json()
  Current_ratio_dictionary[company]['Current_Assets'] = float(BS['financials'][0]['Total current assets'])
  Current_ratio_dictionary[company]['Current_Liabilities'] = float(BS['financials'][0]['Total current liabilities'])
  Current_ratio_dictionary[company]['Current_Ratio'] = Current_ratio_dictionary[company]['Current_Assets']/ Current_ratio_dictionary[company]['Current_Liabilities']

Current_ratio_dictionary

#outcome
{'AAPL': {'Current_Assets': 162819000000.0,
  'Current_Liabilities': 105718000000.0,
  'Current_Ratio': 1.540125617208044},
 'FB': {'Current_Assets': 66225000000.0,
  'Current_Liabilities': 15053000000.0,
  'Current_Ratio': 4.399455258088088},
 'GOOGL': {'Current_Assets': 152578000000.0,
  'Current_Liabilities': 45221000000.0,
  'Current_Ratio': 3.374051878552},
 'MSFT': {'Current_Assets': 175552000000.0,
  'Current_Liabilities': 69420000000.0,
  'Current_Ratio': 2.5288389513108616}}


Current_ratio_dataframe = pd.DataFrame.from_dict(Current_ratio_dictionary, orient='index')

#Graph
import plotly.express as px
fig = px.bar(Current_ratio_dataframe, x=Current_ratio_dataframe.index, y=Current_ratio_dataframe['Current_Ratio'])
fig.show()