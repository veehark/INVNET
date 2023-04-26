import pandas as pd #dataframes
import yfinance as yf #stock data
#if Yahoo does not accept the use of the data, nasdaq-data-link
import numpy as np #data science
import matplotlib.pyplot as plt #calc
import plotly.express as px
import pyfolio as pf
import dash_bootstrap_components as dbc
import dash
from dash import Dash, dcc, html, dash_table

app=dash.Dash()

OMXHGI=yf.download("^GSPC",
                     start=None,
                     end=None,
                     progress=False)

print(OMXHGI.head()) #printing the data frame first rows

OMXHGI=OMXHGI.loc[:,["Adj Close"]]

OMXHGI["simple_rtn"]=OMXHGI["Adj Close"].pct_change()
OMXHGI["log_rtn"]=np.log(OMXHGI["Adj Close"]/OMXHGI["Adj Close"].shift(1))
OMXHGI["cumulative_simple_rtn"]=(OMXHGI["Adj Close"]/OMXHGI.iloc[0]['Adj Close']-1)
OMXHGI=OMXHGI.dropna()
print(OMXHGI.head())

descriptive=pd.DataFrame(OMXHGI.loc[:,'simple_rtn'].describe(include='all'))
print(descriptive)

app.layout=html.Div([
        html.Div(className='row', children='Analysis', style={'textalign':'center', 'color':'#116466', 'fontSize':70}),
            dcc.Graph(figure=px.line(OMXHGI, y='Adj Close')),
                dcc.Graph(figure=px.line(OMXHGI, y='cumulative_simple_rtn')),
                    dcc.Graph(figure=px.line(OMXHGI, y='simple_rtn').update_traces(line_color='gray')),

        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dash_table.DataTable(data=descriptive.to_dict('records'), page_size=8, style_table={'overflowX':'auto'})
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure=px.histogram(OMXHGI, x='simple_rtn', nbins=12000))
        ])
    ])
])

if __name__ == '__main__':
    app.run_server()

