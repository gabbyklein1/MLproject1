import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import plotly.express as px
from KNN_Funct import get_sales_comps
import dash_table
import sys
from KNN_Funct import neighborhood_cluster

clustertext='''### Analysis
This graph gives a better understanding of similar neighborhoods in our Ames dataset. When selecting two clusters, we can see a distinct neighborhood in the mid right. Thats the North Ridge, Stone Bridge area. You can observe based on the Get to know Ames maps that these houses are new and expensive. This is clearly a fancier part of the town, the who's who of Ames, IA, if you will, which is what sets it so apart from other neighborhoods. \n\n
When you increase to three clusters, we see Clear Creek neighborhood stands out in yellow. This neighborhood is interesting because we actually ended up dropping many houses from this neighborhood from our dataset. This was because many of them were more industrial used properties, ie agricultural etc, and were not useful in our model. This distinction is likely why it is set apart in our clustering. \n\n This continues as increasign the cluster numbers, next we see Timbers neighborhood broken out, then BrookDale. Ultimately after feeding these clusters into our stepwise model, we found the most informative was the North Ridge distinciton, as it remained non-zero after penalization.
'''
tdata=pd.read_csv('apps/data/tdata_for_realtor_map.csv')
Neighborhood_as_instance_narrowed=pd.read_csv('apps/data/data_for_clusters.csv')
knn_table_columns=['House','GrLivArea','LotArea','OverallQual','YearBuilt','TotalBsmtSF','GarageArea','Remodeled','SalePrice']
# tdataKNN=pd.read_csv('apps/data/Data_For_KNN_salescomps.csv')
# Miles=2
# numofneighbors=10
# instance=pd.DataFrame({'GrLivArea':1786,   'LotArea':164660,  'OverallQual':5, 'YearBuilt':1965,
# 'TotalBsmtSF':1499,
# 'GarageArea':529,'Lat':41.99854744897959,'Long':-93.6589044489796,
# 'Remodeled':bool(0)}, index=[0])
# KNN_table=get_sales_comps(tdataKNN,instance,Miles,numofneighbors,features=None)
#

SIDEBAR_STYLE = {"position": "fixed", "top": 0, "left": 0,"bottom": 0,
    "width": "16rem", "padding": "2rem 1rem"} #"background-color": "#f8f9fa",


CONTENT_STYLE = {"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem",}
Padded_STYLE = {"margin-left": "-1rem", "margin-right": "2rem","padding": "2rem 1rem",}




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

    html.Div([
        html.Div([html.H3('Real Estate Handbook'),
    dcc.Tabs(id='tabs', value='tab-1', children=[
    dcc.Tab(label='Welcome Realtors!', value='tab-1'),
        dcc.Tab(label='Get to know Ames', value='tab-2'),
        dcc.Tab(label='Research Questions', value='tab-3'),
        dcc.Tab(label='Neighborhood Analysis', value='tab-4'),
        dcc.Tab(label='Sales Comps', value='tab-5'),
    ]),
    html.Div(id='tabs-content', style=Padded_STYLE)
])

], style=CONTENT_STYLE)])


layout = html.Div([sidebar, content])


@app.callback(
    Output('app-4-display-value', 'children'),
    Input('app-4-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)
@app.callback(Output('tabs-content', 'children'),
    Input('tabs', 'value'))
def display_value(value):
    if value=='tab-1':
        return (html.Div([
        html.H3('Welcome Realtors',style={'font-weight': 'bold'}),]),
        dcc.Markdown('''Introducing our Real Estate Handbook, a data rich review of Ames to help real estate agents better understand the market and further assist customers. Here you will find analysis of different house features effect on price as found in our model, a look into the similar and different neighborhoods in Ames, as well as an ML generated sales comps tools for your convenience.'''),
        html.Div([html.Img(src='/assets/shutterstock_752498263-1400x621.jpg')], style={'textAlign': 'center','height':'10%', 'width':'10%'}))
    elif value=='tab-2':
        return (html.Div([
        html.H3('Lets get Ames-icable', style={'font-weight': 'bold'})]),
        dcc.Markdown('''Welcome to Ames, Iowa; named one of the “15 Cities That Have Done the Best Since the Recession” by Bloomberg Business in 2015 and known as the ‘healthiest city in America’ by USA Today. Home to Iowa State University, Ames has become a player in developing the world’s bio-economic future. An attractive location for business, some of the names housed here include 3M, Danfoss, Boehringer Ingelheim, and more. Below, see a simplified map of the houses sold in Ames between 06-09. Interacting with the map will give a general understanding of the city.'''),
        html.Div([html.H3('Visualize the City', style={'font-weight': 'bold'})]),
        dcc.Markdown('''Use this graph to visualize some of the trends of the neighborhood. Use the dropdown menu to color the points by different attributes.'''),
        html.Div([
        dcc.Dropdown(id='dropdown_for_realt_map',options=[{'label': 'Year Built','value': 'YearBuilt'},{'label': 'Gross Living Area', 'value': 'GrLivArea'} ,{'label': 'Sale Price','value': 'SalePrice'},{'label': 'Neighborhood','value': 'Neighborhood'},{'label': 'Overall Quality','value': 'OverallQual'}],value='colorvalue')]),
        dcc.Graph(id='realt_map'))

    elif value=='tab-4':
        return (html.Div([
        html.H3('Neighborhood Clustering', style={'font-weight': 'bold'})]),
        dcc.Markdown('''Below is a tool which helps illustrate which neighborhoods in Ames are most similar. This is helpful to realtors and buyers alike, it gives a sense of comparable neighborhoods to allow a buyer to expand their search. This is also how the neighborhood cluster columns were created in our ML models.'''),
        dcc.Slider(id='sliderforclusters',min=1,max=9,step=None,marks={1: '1',2: '2',3: '3',4: '4',5: '5',6:'6',7:'7',8:'8',9:'9'},value=1),
        dcc.Graph(id='cluster_map'),
        dcc.Markdown(clustertext)
    )
    elif value=='tab-5':
        return (html.Div([
        html.H3('KNN Sales Comps', style={'font-weight': 'bold'})]),
        dcc.Markdown('''This tool uses K-Nearest Neighbors to generate automatic sales comps. Input attributes below to find houses most similar to it and how much they sold for. See below for accepted ranges.'''),
        dcc.Input(id='grlivarea',placeholder='Enter Gross Living Area',type='text',value=''),
        dcc.Input(id='lotarea',placeholder='Enter Lot Area value',type='text',value=''),
        dcc.Input(id='qualval',placeholder='Enter Quality value 1-10',type='text',value=''),
        dcc.Input(id='yearbuiltval',placeholder='Enter Year Built',type='text',value=''),
        dcc.Input(id='bsmtsfval',placeholder='Enter Basement SF',type='text',value=''),
        dcc.Input(id='garageareaval',placeholder='Enter Garage Area',type='text',value=''),
        dcc.Input(id='latval',placeholder='Enter Latitude',type='text',value=''),
        dcc.Input(id='longval',placeholder='Enter Longitude',type='text',value=''),
        dbc.FormGroup([dbc.Label("Remodeled?"),
        dbc.RadioItems(options=[{"label": "True", "value": 1},{"label": "False", "value":0},],value=0,id="remodeledtf",inline=True)], style=Padded_STYLE),
        dcc.Input(id='milerad',placeholder='Enter radius to search (miles)',type='text',value=''),
        html.Hr(),
        html.H3('Sales Comps'),
        dash_table.DataTable(id='knn_table',columns=[{"name": i, "id": i} for i in knn_table_columns],style_cell=dict(textAlign='center')))

@app.callback(
    Output('realt_map', 'figure'),
    Input('dropdown_for_realt_map', 'value'))
def return_realt_map(colorvalue):
    tdata=pd.read_csv('apps/data/tdata_for_realtor_map.csv')
    if colorvalue=='YearBuilt':
        return px.scatter(tdata, x="Lat", y="Long", color='YearBuilt',title="Houses Sold in Ames Iowa \'06-\'09'")
    elif colorvalue=='GrLivArea':
        return px.scatter(tdata, x="Lat", y="Long", color='GrLivArea',title="Houses Sold in Ames Iowa \'06-\'09'")
    elif colorvalue=='SalePrice':
        return px.scatter(tdata, x="Lat", y="Long", color='SalePrice',title="Houses Sold in Ames Iowa \'06-\'09")

    elif colorvalue=='Neighborhood':
        return px.scatter(tdata, x="Lat", y="Long", color='Neighborhood',title="Houses Sold in Ames Iowa \'06-\'09")
    elif colorvalue=='OverallQual':
        return px.scatter(tdata, x="Lat", y="Long", color='OverallQual',title="Houses Sold in Ames Iowa \'06-\'09")
    else:
        return px.scatter(tdata, x="Lat", y="Long",title="Houses Sold in Ames Iowa \'06-\'09")

@app.callback(
    Output('knn_table', 'data'),
    [Input('grlivarea', 'value'),
    Input('lotarea', 'value'),
    Input('qualval', 'value'),
    Input('yearbuiltval', 'value'),
    Input('bsmtsfval', 'value'),
    Input('garageareaval', 'value'),
    Input('remodeledtf', 'value'),
    Input('latval', 'value'),
    Input('longval', 'value'),
    Input('milerad', 'value')])
def return_knn(valuegr,valuela,valuequality,valueyearbuilt,valuebsmtsf,valuegarage,valueremodeled,valuelat,valuelong,milerad):
    tdata=pd.read_csv('apps/data/Data_For_KNN_salescomps.csv')
    Miles=milerad
    numofneighbors=10
    # if valuela=='' or valuegr=='' or valuequality=='' or valueyearbuilt=='' or valuebsmtsf=='' or valuegarage=='' or valuelat=='' or valuelong=='':
    #     instance=pd.DataFrame({'GrLivArea':1786,   'LotArea':164660,  'OverallQual':5, 'YearBuilt':1965,
    #     'TotalBsmtSF':1499,
    #     'GarageArea':529,'Lat':41.99854744897959,'Long':-93.6589044489796,
    #     'Remodeled':bool(0)}, index=[0])
    #
    instance=pd.DataFrame({'GrLivArea':valuegr,   'LotArea':valuela,  'OverallQual':valuequality, 'YearBuilt':valueyearbuilt,
    'TotalBsmtSF':valuebsmtsf,
    'GarageArea':valuegarage,'Lat':valuelat,'Long':valuelong,
    'Remodeled':bool(valueremodeled)}, index=[0])
    # instance=pd.DataFrame({'GrLivArea':1786,   'LotArea':164660,  'OverallQual':5, 'YearBuilt':1965,
    # 'TotalBsmtSF':1499,
    # 'GarageArea':529,'Lat':41.99854744897959,'Long':-93.6589044489796,
    # 'Remodeled':bool(0)}, index=[0])
    KNN_table=get_sales_comps(tdata,instance,Miles,numofneighbors,features=None)
    return KNN_table.to_dict('records')

@app.callback(
    Output('cluster_map', 'figure'),
    Input('sliderforclusters', 'value'))
def return_cluster_map(sliderforclusters):
    df=neighborhood_cluster(sliderforclusters)
    return px.scatter(df, x="Lat", y="Long", color='Label',title="Clustered Neighborhood Map")
