import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

from app import app

# DataFrame for the table
coefs_df = pd.read_csv('stepwise_coefs_dash.csv', index_col=False)

# Already fitted model for the prediction of home prices.
ols = pd.read_pickle('stepwise_model.pickle')




model_details = '''
When testing various models, we found that many different types of models performed rather similarly. 
We ended up choosing a simple linear regression with features chosen through step-wise feature selection. 
This resulted in a model with 31 features (down from the 87 in our dataset prepped for machine learning) 
that showed similar predictive power to more complex models, while maintaining the 
interpretability of its calculations.\n

\nThe features used in the model, and their coefficients, can be found in the accompanying table. 
Unsurprisingly, We found the most important features to be the size of the house, its age, 
and its overall quality. Something that did surprise us was that our model did not select to use 
the number of bathrooms in a house as a feature. When we attempted to add this to the model, it increased 
multicollinearity between features while adding no predictive power. This signals that the number of 
bathrooms in a house can be predicted based on the features already used in the model, including size 
and age of the home. \n

\nThe model resulted in a test R^2 of 0.920 and a residual standard error of $19,390. 
While this error is very large compared to the average profit per house estimate of 1.3% in instant 
home buying programs, we assume this would add variance to our per-home profit and not result in systematic 
mispricing. Future collection of more home sale records in Ames would likely reduce our residual 
standard error significantly, resulting in an even more accurate model.

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



tab1_content = html.Div([
    html.H2('Model Interpretation', style={'textAlign': 'center'}),
    dbc.Row([dbc.Col([html.H5('The Pricing model:'),
        dcc.Markdown(model_details)]),
        dbc.Col([dash_table.DataTable(
            id='coefs_table',
            columns=[{"name": i, "id": i} 
                 for i in coefs_df.columns],
            data=coefs_df.to_dict('records'),
            style_cell_conditional=[
                {'if': {'column_id': c},
                'textAlign': 'left'
                } for c in ['Feature']
                ],
            style_header={
                'backgroundColor': 'DarkGray',
                'fontWeight': 'bold',
                'color': 'black'},
            style_cell={
                'backgroundColor': 'Gainsboro',
                'color': 'black'},
    style_as_list_view=True,
            )]),      
        ])
], style=CONTENT_STYLE)



tab2_content = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.H2('Pricing Dashboard: Set House Attributes', style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([html.Div('GrLivArea'),
                dcc.Input(
                    id='GrLivArea-input',
                    placeholder='Enter a value (in sqft)...',
                    type='text',
                    value='1430')
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BedroomAbvGr'),
                dcc.Slider(
                    id='BedroomAbvGr-input',
                    min=0,
                    max=10,
                    step=1,
                    marks={i: '{}'.format(i) for i in range(1,11)},
                    value=3)  # Check average bedrooms count
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Dist_From_UoI'),
                dcc.Input(
                    id='Dist_From_UoI-input',
                    placeholder='Enter a value (in km)...',
                    type='text',
                    value='2.93')
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('BldgType_Twnhs', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BldgType_Twnhs-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BldgType_TwnhsE', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BldgType_TwnhsE-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('LotArea', style={'textAlign': 'center'}),
                dcc.Input(
                    id='LotArea-input',
                    placeholder='Enter a value (in sqft)...',
                    type='text',
                    value='9500')
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('Condition1_Artery', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Condition1_Artery-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Exterior1st_AsbShng', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Exterior1st_AsbShng-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Exterior1st_BrkFace', style={'textAlign': 'center'}),
                 dcc.RadioItems(
                    id='Exterior1st_BrkFace-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('Exterior1st_HdbdOther', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Exterior1st_HdbdOther-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Foundation_Wood', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Foundation_Wood-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('YearBuilt', style={'textAlign': 'center'}),
                dcc.Input(
                    id='YearBuilt-input',
                    placeholder='Enter a value...',
                    type='text',
                    value='1973')
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('OverallQual', style={'textAlign': 'center'}),
                dcc.Slider(
                    id='OverallQual-input',
                    min=0,
                    max=10,
                    step=1,
                    marks={i: '{}'.format(i) for i in range(1,11)},
                    value=6) 
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('OverallCondBinary', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='OverallCondBinary-input',
                    options=[
                        {'label': 'Average or above  |', 'value': 0},
                        {'label': 'Below Average', 'value': 1}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('ExterQual_Ex', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='ExterQual_Ex-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('ExterQual_Gd', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='ExterQual_Gd-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('KitchenQual_Ex', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='KitchenQual_Ex-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('RemodelYrsAftBuilt', style={'textAlign': 'center'}),
                dcc.Input(
                    id='RemodelYrsAftBuilt-input',
                    placeholder='Enter a value...',
                    type='text',
                    value='0')
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('Functional_Min', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Functional_Min-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Functional_Maj', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Functional_Maj-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BsmtQual_None', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BsmtQual_None-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),  ## Maybe change to be more natural of a question.
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('TotalBsmtSF', style={'textAlign': 'center'}),
                dcc.Input(
                    id='TotalBsmtSF-input',
                    placeholder='Enter a value...',
                    type='text',
                    value='960')
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BsmtUnfSF', style={'textAlign': 'center'}),
                dcc.Input(
                    id='BsmtUnfSF-input',
                    placeholder='Enter a value...',
                    type='text',
                    value='450')
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BsmtFinGdLvng', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BsmtFinGdLvng-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('BsmtExposure', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BsmtExposure-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('BsmtQual_Ex', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='BsmtQual_Ex-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('GarageArea', style={'textAlign': 'center'}),
                dcc.Input(
                    id='GarageArea-input',
                    placeholder='Enter a value...',
                    type='text',
                    value='470')
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('GarageFinish_RFn', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='GarageFinish_RFn-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('Fireplaces', style={'textAlign': 'center'}),
                dcc.Slider(
                    id='Fireplaces-input',
                    min=0,
                    max=5,
                    step=1,
                    marks={i: '{}'.format(i) for i in range(0,6)},
                    value=0) 
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div('SchD_S', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='SchD_S-input',
                    options=[
                        {'label': 'One     |', 'value': 0},
                        {'label': 'Five', 'value': 1}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([html.Div('Neighborhood Cluster Label_3', style={'textAlign': 'center'}),
                dcc.RadioItems(
                    id='Neighborhood Cluster Label_3-input',
                    options=[
                        {'label': 'Yes     |', 'value': 1},
                        {'label': 'No', 'value': 0}
                        ],
                    value=0,
                    labelStyle={'display': 'inline-block'})
                ], style={'textAlign': 'center'}),
                dbc.Col([ html.Button('Calculate Value', id='button', n_clicks=0)
                ], style={'textAlign': 'center'}),
                dbc.Col([html.Div(id='price-prediction'),
                ], style={'textAlign': 'center'}),
            ]), 
        ]), style=CONTENT_STYLE
    ),
    dbc.Card(
        dbc.CardBody([
            html.H2('The Predicted Home Value Is:', style={'textAlign': 'center'}),
            html.H1(id='price-prediction', style={'textAlign': 'center'}),
            ]), style=CONTENT_STYLE
        )
])


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Model Interpretation"),
        dbc.Tab(tab2_content, label="Model Dashboard")
    ], style=CONTENT_STYLE
)



layout = html.Div([sidebar, tabs])



@app.callback(
    Output('price-prediction', 'children'),
    Input('button', 'n_clicks'),
    State('GrLivArea-input', 'value'),
    State('BedroomAbvGr-input', 'value'),
    State('Dist_From_UoI-input', 'value'),
    State('BldgType_Twnhs-input', 'value'),
    State('BldgType_TwnhsE-input', 'value'),
    State('LotArea-input', 'value'),
    State('Condition1_Artery-input', 'value'),
    State('Exterior1st_AsbShng-input', 'value'),
    State('Exterior1st_BrkFace-input', 'value'),
    State('Exterior1st_HdbdOther-input', 'value'),
    State('Foundation_Wood-input', 'value'),
    State('YearBuilt-input', 'value'),
    State('OverallQual-input', 'value'),
    State('OverallCondBinary-input', 'value'),
    State('ExterQual_Ex-input', 'value'),
    State('ExterQual_Gd-input', 'value'),
    State('KitchenQual_Ex-input', 'value'),
    State('RemodelYrsAftBuilt-input', 'value'),
    State('Functional_Min-input', 'value'),
    State('Functional_Maj-input', 'value'),
    State('BsmtQual_None-input', 'value'),
    State('TotalBsmtSF-input', 'value'),
    State('BsmtUnfSF-input', 'value'),
    State('BsmtFinGdLvng-input', 'value'),
    State('BsmtExposure-input', 'value'),
    State('BsmtQual_Ex-input', 'value'),
    State('GarageArea-input', 'value'),
    State('GarageFinish_RFn-input', 'value'),
    State('Fireplaces-input', 'value'),
    State('SchD_S-input', 'value'),
    State('Neighborhood Cluster Label_3-input', 'value'))
def predict_homeval(clicks, GrLivArea, BedroomAbvGr, Dist_From_UoI, BldgType_Twnhs, BldgType_TwnhsE, LotArea, \
    Condition1_Artery, Exterior1st_AsbShng, Exterior1st_BrkFace, Exterior1st_HdbdOther, Foundation_Wood, YearBuilt, \
    OverallQual, OverallCondBinary, ExterQual_Ex, ExterQual_Gd, KitchenQual_Ex, RemodelYrsAftBuilt, Functional_Min, \
    Functional_Maj, BsmtQual_None, TotalBsmtSF, BsmtUnfSF, BsmtFinGdLvng, BsmtExposure, BsmtQual_Ex, GarageArea, \
    GarageFinish_RFn, Fireplaces, SchD_S, Neighborhood_Cluster_Label_3):
    # This will be used to create the observation to predict upon, then run it through the model.
    house=np.array([int(GrLivArea), int(TotalBsmtSF), int(YearBuilt), OverallQual, ExterQual_Ex, int(BsmtUnfSF), \
        int(RemodelYrsAftBuilt), KitchenQual_Ex, BsmtQual_Ex, int(GarageArea), Neighborhood_Cluster_Label_3, \
        BldgType_TwnhsE, int(LotArea), BsmtExposure, BedroomAbvGr, OverallCondBinary, Functional_Maj, ExterQual_Gd, \
        Functional_Min, Fireplaces, BsmtFinGdLvng, SchD_S, float(Dist_From_UoI), BldgType_Twnhs, Condition1_Artery, \
        BsmtQual_None,Exterior1st_HdbdOther, Exterior1st_BrkFace, GarageFinish_RFn, Foundation_Wood, Exterior1st_AsbShng])
    # Return the predicted value    
    return round(ols.predict(house.reshape(1, -1))[0],0)

# @app.callback(
#     Output('home_text', 'value'),
#     State('price-prediction', 'value'),
#     Input('button', 'n_clicks'))
# def HomeText(n_clicks, homePrice):
#     if n_clicks<1:
#         return ''
#     return f''
