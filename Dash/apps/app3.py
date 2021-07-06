import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app



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


content = html.Div([
    html.H3('App 3'),
    dcc.Dropdown(
        id='app-3-dropdown',
        options=[
            {'label': 'App 3 - {}'.format(i), 'value': i} for i in [
                'Why?', 'Why Not?', 'Dummy or Smarty?'
            ]
        ]
    ),
    html.Div(id='app-3-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
], style=CONTENT_STYLE)

layout = html.Div([sidebar, content])


@app.callback(
    Output('app-3-display-value', 'children'),
    Input('app-3-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)