import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

from app import app

coefs_df = pd.read_csv('stepwise_coefs_dash.csv', index_col=False)

SIDEBAR_STYLE = {"position": "fixed", "top": 0, "left": 0,"bottom": 0,
    "width": "16rem", "padding": "2rem 1rem"} #"background-color": "#f8f9fa",


CONTENT_STYLE = {"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem",}

sidebar = html.Div([
        html.H2("Housing Prices in Ames, Iowa", style={'textAlign': 'center'}), 
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Introduction", href="/apps/app1", active="exact"), 
                dbc.NavLink("Project", href="/apps/app2", active="exact"),
                dbc.NavLink("Pricing Model", href="/apps/app3", active="exact"),
                dbc.NavLink("Real Estate Handbook", href="/apps/app4", active="exact"),
                dbc.NavLink("Miscellaneous", href="/apps/app5", active="exact"),
            ], vertical=True, pills=True
        )
    ],
    style=SIDEBAR_STYLE,
)



tab1_content = html.Div([
    html.H2('Model Interpretation'),
    dash_table.DataTable(
        id='coefs_table',
        columns=[{"name": i, "id": i} 
                 for i in coefs_df.columns],
        data=coefs_df.to_dict('records'),
        style_cell=dict(textAlign='center')#,
        #style_header=dict(backgroundColor="paleturquoise"),
        #style_data=dict(backgroundColor="lavender")
    )
], style=CONTENT_STYLE)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2('Dashboard', style={'textAlign': 'center'}),
            dcc.Markdown('Model Dashboard goes here.')
        ]
    ), style=CONTENT_STYLE
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Model Interpretation"),
        dbc.Tab(tab2_content, label="Model Dashboard")
    ], style=CONTENT_STYLE
)



layout = html.Div([sidebar, tabs])



@app.callback(
    Output('app-3-display-value', 'children'),
    Input('app-3-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)