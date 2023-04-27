import pandas as pd #dataframes
import yfinance as yf #stock data
#if Yahoo does not accept the use of the data, nasdaq-data-link
import numpy as np #data science
import matplotlib.pyplot as plt #calc
import plotly.express as px
import plotly.graph_objects as go
import pyfolio as pf
import dash_bootstrap_components as dbc
import dash
from dash import Dash, dcc, html, dash_table

app=Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Data downloading
ticker="^OMXHGI"

OMXHGI=yf.download(ticker,
                     start=None,
                     end=None,
                     progress=False)

OMXHGI=OMXHGI.loc[:,["Adj Close"]]

#Return calculations
OMXHGI["simple_rtn"]=OMXHGI["Adj Close"].pct_change()
OMXHGI["log_rtn"]=np.log(OMXHGI["Adj Close"]/OMXHGI["Adj Close"].shift(1))
OMXHGI["cumulative_simple_rtn"]=(OMXHGI["Adj Close"]/OMXHGI.iloc[0]['Adj Close']-1)
OMXHGI=OMXHGI.dropna()

#Building graphs and tables
table_desc=pd.DataFrame(OMXHGI.loc[:,'simple_rtn'].describe(include='all'))

fig_price=px.line(OMXHGI, y='Adj Close')
fig_price.update_layout(margin=dict(l=2, r=2, b=5, t=5), xaxis=dict(showspikes=True,
                            spikethickness=1,
                            spikedash='dot',
                            spikemode='across'))

fig_rtn=px.line(OMXHGI, y='simple_rtn').update_traces(line_color='gray')
fig_rtn.update_layout(margin=dict(l=2, r=2, b=5, t=5), xaxis=dict(showspikes=True,
                            spikethickness=1,
                            spikedash='dot',
                            spikemode='across'))

fig_hist=px.histogram(OMXHGI, x='simple_rtn', nbins=1000)
fig_hist.update_layout(margin=dict(l=2, r=2, b=5, t=5), xaxis=dict(showspikes=True,
                            spikethickness=1,
                            spikedash='dot',
                            spikemode='across'))

#Dash building
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_price, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_rtn, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6)
    ], justify="between"),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(table_desc.to_dict('records'),
                                 [{"name": i, "id": i} for i in table_desc.columns])
        ], width=3),
        dbc.Col([
            dcc.Graph(figure=fig_hist, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6)
    ], justify="between"),
])

if __name__ == '__main__':
    app.run_server()

