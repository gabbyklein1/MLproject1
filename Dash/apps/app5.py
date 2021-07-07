import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import dash_table

from app import app

future_work = '''
Placeholder for the long talk on future work for this project. Should be a considerable amount of text.
'''


ml_intercept_text = '''
---
Heating quality and condition (HeatingQC) - Excellent drops to the intercept, other categories in our 
analysis are good, typical, and fair.\n
---
Central Air (NoCentralAir) - Homes with central air drop to intercept, we have a category for 
houses that lack central air.\n
---
Electrical System (NonStdElectrical) - Homes with standard circuit breakers and romex drop to the 
intercept, we have another category for non-standard electrical systems, which includes: \n
(a) Fuse Box over 60 AMP and all Romex wiring, \n
(b) 60 AMP Fuse Box and mostly Romex wiring, \n
(c) 60 AMP Fuse Box and mostly knob & tube wiring, and \n
(d) Mixed.\n
---
Kitchen quality (KitchenQual) - Typical-quality drops to the intercept. Other categories in our analysis 
are excellent, good, and fair.\n
---
Home Functionality (Functional) - Typical functioning homes drop to the intercept. Our other 
two categories are negative adjustments to this, (a) minor deductions, and (b) a group including 
moderate and major deductions as well as salvage-only homes.\n
---
Roof type (RoofStyle) - Gable roofs drop to the intercept. We have two other categories in our 
analysis, (a) hip-style roofs and (b) roofs of other styles (barn, flat, mansard, and shed).\n
---
Exterior covering on the house (Exterior1st) - Homes with exterior coverings of vinyl siding, plywood, 
or brick common drop to the intercept (highest-value coverings). This dividing of coverings required 
domain knowledge. Other categories of middling value are (a) Brick face, (b) metal siding, 
(c) Stucco / cement board / wood siding / wood shingles. Categories of low value are (a) 
hardboard / other (imitation stucco, asphalt shingles,  precast, and cinderblock), and (b) asbestos shingles. 
Asbestos shingles are the worst, they have been illegal since the 70’s and are costly to replace with more 
modern, safer materials. \n
---
Masonry veneer type (MasVnrType) - Homes without masonry veneer drop to the intercept. Our other categories 
are (a) homes with brick-face veneer, and (b) homes with either stone or brick-common veneer (more 
valuable than brick-face). \n
---
Foundation type (Foundation) - Homes with cinder block foundations drop to the intercept. Other categories 
we have in our analysis are (a) poured concrete, (b) brick and tile, (c ) slab, (d) stone, and (e) wood. \n
---
**Height of basement (BsmtQual)** - Homes with basement heights of 80-89 inches drop to the intercept. Other 
categories are (a) 100+ inches high, (b) 90-99 inches, (c) less than 79 inches high, and (d) homes with no basements.\n
---
**General condition of basement (BsmtCond)** - Homes with typical basement d=condition with slight dampness 
allowed drop to the intercept. Other categories are (a) good condition (better than typical), (b) basements 
with dampness, some settling or cracking, or severe settling/cracking/wetness, and (c ) homes with no basements.\n
---
**Basements with walkouts or garden-level walls (BsmtExposure)** - Homes without garden-level walls or walkouts 
drop to the intercept. Our other category is homes with garden-level walls or walkouts.\n
---
**Basements with good finished living quarters (BsmtFinGdLvng)** - Homes without good finished basement living 
quarters drop to the intercept. Our other category is homes with good finished basement living quarters.\n
---
**Fireplace Quality (FireplaceQu)** - Homes without fireplaces drop to the intercept. Our other categories are 
(a) homes with exceptional masonry fireplaces, (b) homes with masonry fireplaces in the main level, (c ) homes 
with prefabricated fireplaces in the main level, (d) homes with prefabricated fireplaces in the basement, 
and (e) homes with Ben Franklin stoves.\n
---
**Type of Garage (GarageType)** - Homes with attached garages (including built-in and basement) drop to the 
intercept. Our other categories are homes without garages, and homes with detached garages.\n
---
**Finish of the garage (GarageFinish)** - Homes with unfinished garages drop to the intercept. Our other 
categories are (a) homes with rough-finished garages, and (b) homes with finished garages.\n
---
**Driveway finish (PavedDrive)** - Homes with unpaved drives drop to the intercept. Our other category 
is homes with paved driveways.\n
---
**Wood deck (WoodDeckBinary)** - Homes without a deck drop to the intercept. Our other category is homes 
with a wood deck.\n
---
**Porch (HasPorch)** - Homes without a porch drop to the intercept. Our other category is homes with a porch.\n
---
**Fencing (FenceBinary)** - Homes without fencing drop to the intercept. Our other category is homes with a fence.\n
---
**Overall condition of the house (OverallCondBinary)** - Homes in average to very excellent condition drop to 
the intercept (average+). Our other category is homes that have below average to very poor condition.\n
---
**School District (SchD_S)** - Homes in the school district 1 in our dataset drop to the intercept. Our other 
category is homes in the school district 5.\n
---
**Number of stories (MSSubClass)** - One-story homes drop to the intercept (includes one-story homes with 
finished attics, split-level homes and split-foyer homes). Our other category is homes with more than one 
story (includes 1.5-story homes, 2-story homes, 2.5-story homes, and multi-level homes). \n
---
**Lot Shape  (LotShape)** -  Lots with a regular general shape drop to the intercept. Our other category is 
lots that are irregularly shaped.\n
---
**Lot slope (SlopedLot)** - Homes with level lots drop to the intercept. Our other category is sloped lots, 
which are either banked, on a hillside, or in a depression.\n
---
**Configuration of the lot (LotConfig)** - Homes that are on inside lots (neighbors on both sides) drop to the 
intercept. Our other categories are homes that are on (a) corner lots, or (b) cul de sacs.\n
---
**Proximity to various items (Condition1)** - Homes that are not near special features drop to the intercept. 
Our other categories are homes that (a) are within 200’ of a railroad, (b) are near positive off-site 
features such as parks, (c ) are adjacent to feeder streets, and (d) are adjacent to arterial streets.\n
---
**Building type (BldgType)** - Home that are single-family homes drop to the intercept. Our other 
categories are (a) townhouse end units, and (b) townhouse inside units.\n
---
**Quality of the material on the exterior (ExterQual)** - Homes with typical-quality exterior materials 
drop to the intercept. Our other categories are homes with (a) Excellent quality exterior materials, (b) good 
quality exterior materials, (c ) fair quality exterior materials, and (d) poor quality exterior materials. \n
---
**Neighborhood (Neighborhood)** - Homes not in the top 15 most represented neighborhoods in our home sales 
data were grouped together and drop to the intercept. Our other categories are the names of the 15 most 
represented neighborhoods.
'''




df1 = pd.read_csv('apps/data/merge_data_update.csv', index_col=0)

df2 = pd.read_csv('apps/data/RowFiltered_condensed_data_TRAIN_subsect.csv', index_col=False)
df3 = pd.read_csv('apps/data/RowFiltered_condensed_data_TRAIN.csv', index_col=False)


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

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2('Future Work', style={'textAlign': 'center'}),
            dcc.Markdown(future_work)
        ]
    ), style=CONTENT_STYLE
)


#tab1_content = html.Div([
#    html.H2('Future Work', style={'textAlign': 'center'}),
#    dcc.Markdown(future_work)
#], style=CONTENT_STYLE
#)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2('Machine Learning Intercept Analysis', style={'textAlign': 'center'}),
            dcc.Markdown(ml_intercept_text)
        ]
    ), style=CONTENT_STYLE
)


tab3_content = dbc.Card(
    dbc.CardBody([

            html.H2('Original Data Set', style={'textAlighn': 'center'}),
            html.Div(
    [html.Button("Download Data", id="btn_txt"), dcc.Download(id="download-text")]),

    ]), style=CONTENT_STYLE
)



tab4_content = dbc.Card(
    dbc.CardBody([

            html.H2('Transformed Data Train Set', style={'textAlighn': 'center'}),
        dash_table.DataTable(
            id='Transformed Data Train Set',
            columns=[{'name': i, 'id': i} for i in df2.columns],
            data=df2.to_dict('records'),
            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'}

        ),html.Div(
        [html.Button("Download Data", id="btn_txt_rowfilt"), dcc.Download(id="download-text_rowfilt")])
    ]), style=CONTENT_STYLE
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Future Work"),
        dbc.Tab(tab2_content, label="Data Dictionary"),
        dbc.Tab(tab3_content, label="Original Data Set"),
        dbc.Tab(tab4_content, label='Transformed Data Set')
    ], style=CONTENT_STYLE
)





layout = html.Div([sidebar, tabs])

@app.callback(
    Output("download-text", "data"),
    Input("btn_txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df1.to_csv, "AmesIowadf.csv")

@app.callback(
    Output('app-5-display-value', 'children'),
    Input('app-5-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output("download-text_rowfilt", "data"),
    Input("btn_txt_rowfilt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df3.to_csv, "AmesIowadf_rowfilt.csv")
