import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import os
api_key = os.getenv('api_key')

app = dash.Dash()

app.layout = html.Div([
  html.H1('Financial Dashboard'),

  html.Div([  
  dcc.Input(id='company_selection',value='AAPL'),
  html.H3(id='text'),
  dcc.Graph(id ='revenue'),
  dcc.Graph(id ='netincome'),
  ],style= {'padding':10})
])


@app.callback(Output('revenue','figure'),
              [Input('company_selection','value')])
def retrieve_revenue(company):
  demo = api_key
  stock = company
  print(stock)
  IS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey={demo}')
  IS = IS.json()
  IS = IS['financials']
  Revenues = []
  Dates = []
  count = 0
  for item in IS:
    Revenues.append(float(IS[count]['Revenue']))
    Dates.append(IS[count]['date'])
    count += 1
  print(Revenues)
  datapoints = {'data': [go.Bar(x=Dates, y=Revenues)],'layout': dict(xaxis={'title':'Date'},
                                                                      yaxis={'title':'Revenue'},
                                                                            )}


  return datapoints


@app.callback(Output('netincome','figure'),
              [Input('company_selection','value')])
def retrieve_revenue(company):
  demo = 'your api key'
  stock = company
  IS = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey={demo}')
  IS = IS.json()
  IS = IS['financials']
  Revenues = []
  Dates = []
  count = 0
  for item in IS:
    Revenues.append(float(IS[count]['Net Income']))
    Dates.append(IS[count]['date'])
    count += 1
 
  datapoints = {'data': [go.Bar(x=Dates, y=Revenues,marker_color='lightsalmon',name='Net Income')],
  'layout': dict(xaxis={'title':'Date'},
                yaxis={'title':'Net Income'},
                  )}
  return datapoints


@app.callback(
    Output(component_id='text', component_property='children'),
    [Input(component_id='company_selection', component_property='value')]
)
def update_output_div(input_value):
    return 'Displaying Data for "{}"'.format(input_value)
if __name__ == '__main__':
    app.run_server(debug=True)