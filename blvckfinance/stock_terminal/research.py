import requests
import pandas as pd
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import os
api_key = os.getenv('api_key')

def income_statement(stock):
	#put in separate file
 	#api_key = '6dd9e2948898d127fc9'
 	number_qts = input('number_qts').strip()
 	IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit={number_qts}&apikey={api_key}').json()
 	IS = pd.DataFrame.from_dict(IS)
 	print(IS.T)
 	save_to_csv = input('save_to_csv? y or n').strip()
 	if save_to_csv == 'y':
 		IS.to_csv('BS.csv')
    
while True:
    comman = input('stock?')
    stock = comman.split(' ')[1]
    if comman == 'IS ' + stock :
        income_statement(stock)
    elif comman == 'quit':
        break
    else:
        print('Invalid Command.')