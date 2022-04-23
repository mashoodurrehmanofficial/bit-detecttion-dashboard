
from click import style
from dash import Input, Output, html,dcc,dash_table, Input, Output
from  dash import * 
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go 
from urllib.parse import urlparse

import plotly.express as px
import plotly,os


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Traffic Analysis"

# df = pd.read_excel(open("data.xlsx",'rb'), sheet_name='Sheet1')


left_panel = html.Div(
    [html.H1("My name is ali",className='sticky-top',style={"position": "absolute",'top': '0'})]+[
        html.H1("Hello"), 
    ]*20   ,
    className='',
)
    

main_row = dbc.Row(
    [
        dbc.Col(left_panel, className='p-0 m-0  bg-success hidden_scroll_bar', style={"height":"100%"}),
        dbc.Col("hello",  className='p-0 m-0  bg-danger'), 
    ],
    className='p-0 m-0 bg-light vh-100', 
)





#  Main Container
app.layout = html.Div(
    main_row
)

if __name__ == "__main__":
    app.run_server(debug=True)
