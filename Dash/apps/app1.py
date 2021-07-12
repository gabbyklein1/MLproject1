import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


intro_text = '''
Welcome to our application! This was produced as part of an NYC Data Science Academy project.
In this app, we will implement machine learning models to price homes in Ames, Iowa and provide insight into the
real estate market there. To direct our project efforts we adopted the approach of working for Zillow Offers, a relatively new
instant home buying service from Zillow.
'''

gabby_bio = '''
Gabby is a recent graduate of the University of Chicago with a Masters in Applied Mathematics.
She is currently an NYC Data Science Academy fellow and is looking forward to using her analytical
background in launching a career in data science. She loves a good math puzzle which contributes to her passion for data science.
'''


jude_bio = '''
Aditya is a Data Science Fellow at NYC Data Science Academy with hopes of paving a new pathway in his career journey. A graduate from Drexel University with a B.S. in Entertainment & Arts Management. Previous experience includes working in marketing and promotions at Entercom Communication in NYC. With a new horizon in sight, Aditya looks forward to creating a name for himself as a Data Scientist.
'''

ryan_bio = '''
Ryan Burakowski is a current NYC Data Science Academy fellow with experience
in capital markets and a passion for working on difficult problems. He has a B.S. in
Chemical Engineering from Brown University and is excited to make data analytics a
cornerstone of his career moving forward.
'''

organize_text = '''
**This application is divided into several sections.**
- The **'Project'** section provides some context to the project and a walk-through of the analysis undertaken.
- The **'Pricing Model'** section focuses on the machine learning model selected to perform the task of providing
prices for the Zillow Offer, and includes a dashboard for entering in home details to produce an estimated fair value.
- The **'Real Estate Handbook'** section includes insights gleaned from our exploration of the Ames, Iowa housing
market. It is meant to be used by Zillow Preferred Agents to help them provide even more value to their clients.
- The **'Miscellaneous'** section includes information on future extensibility of the project as well as a data
dictionary for reference.
'''








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
    html.H3('Pricing Homes in Ames, Iowa using Machine Learning'),
    html.P(intro_text),
    html.Hr(),
    html.H3('Meet the Authors!', style={'textAlign': 'center'}),
    dbc.Row(
            [
                dbc.Col([html.Div([html.B("Gabby Klein")], style={'textAlign': 'center'}),
                html.Div([html.Img(src='/assets/Gabby_pic.jpg')], style={'textAlign': 'center'}),
                html.P(gabby_bio)
                ]),
                dbc.Col([html.Div([html.B("Aditya Jayasuri")], style={'textAlign': 'center'}),
                html.Div([html.Img(src='/assets/Jude_pic.jpg')],style={'textAlign': 'center'}),
                html.P(jude_bio)
                ]),
                dbc.Col([html.Div([html.B("Ryan Burakowski")], style={'textAlign': 'center'}),
                html.Div([html.Img(src='/assets/ryan_pic.jpg')], style={'textAlign': 'center'}),
                html.P(ryan_bio)
                ]),
            ]),
    html.Hr(),
    html.H3('Layout of the App'),
    dcc.Markdown(organize_text),

], style=CONTENT_STYLE)


## This is how the sidebar and content is displayed together
layout = html.Div([sidebar, content])
