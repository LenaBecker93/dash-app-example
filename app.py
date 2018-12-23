
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df_origin = pd.read_csv('nama_10_gdp_1_Data.csv')

#remove European union and Euro area
df_filtered = df_origin[~df_origin['GEO'].str.contains('Euro')]

#remove everything that is not UNIT Current prices, million euro 
df = df_filtered[df_filtered['UNIT'].str.contains('Current prices, million euro')]

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

colors = {
    'background' : '#6f0038',#'#4B0082',
    'white' : '#FFFFFF',
    'black' : '#000000',
    'linesdots' : '#6f0038', #'#00BFFF' #
    'graphs' : '#ffd8ec'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    #part1
    html.Div([
        html.H1(
            children = 'eurostat Dashboard - GDP and main components',
            style = {'font-size': '25px', 'text-align': 'center', 'color': colors['white']}
        ),
        html.H1(
            children = 'Overview',
            style = {'font-size': '18px', 'text-align': 'center', 'color': colors['white']}
        ),
        html.Div([
            html.H1(
            children = 'Select  indicator for  x axis [Current prices, million euro]',
            style = {'font-size': '14px', 'text-align': 'left', 'color': colors['white']}
            ),
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services',
                ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block', 'color': colors['white']}
            )
        ],style={'width': '35%', 'display': 'inline-block', 'margin' : '10px 40px'},
        ),
        html.Div([
            html.H1(
            children = 'Select  indicator for  y axis [Current prices, million euro]',
            style = {'font-size': '14px', 'text-align': 'left', 'color': colors['white']}
            ),
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block', 'color': colors['white']}
            )
        ],style={'width': '35%', 'float': 'right', 'display': 'inline-block', 'margin' : '10px 40px'})
    ],
    ),
    
    html.Div([
        dcc.Graph(
            id='indicator-graphic1',
            clickData={'points': [{'text': 'Spain'}]},
            style={"height" : 300, 'color': colors['white'], 'backgroundColor': colors['graphs']}
        ),
    ], style = {'margin' : '10px 20px'}
    ),
    
    html.Div([
        dcc.Slider(
            id='year--slider1',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): {'label' : str(year), 'style': {'color': colors['white']}} for year in df['TIME'].unique()},
        ),
        ], style = {'margin' : '10px 60px', 'color': colors['white']}
    ),
    
    #part2
    html.Div([
        html.H1(
            children = 'Space',
            style = {'font-size': '25px', 'text-align': 'center', 'color': colors['background']}
        ),
        html.H1(
            children = 'Chronological development of an indicator per country from 2008 to 2017',
            style = {'font-size': '18px', 'text-align': 'center', 'color': colors['white']}
        ),
        html.Div([
            #Dropdown for countries
            html.H1(
                children = 'Select another country by clicking on a dot in the first graph',
                style = {'font-size': '14px', 'text-align': 'left', 'color': colors['white']}
            ),
            html.H1(
                id='country',
                style = {'font-size': '20px', 'text-align': 'left', 'color': colors['black'], 'backgroundColor': colors['white']}
            )
            #dcc.Dropdown(
            #    id='dropdown_countries2',
            #    options=[{'label': i, 'value': i} for i in available_countries],
            #    value='Belgium'
            #)         
        ],style={'width': '35%', 'display': 'inline-block', 'margin' : '10px 40px'}),
        
        html.Div([
            #Dropdown for indicators for y axis
            html.H1(
                children = 'Select  indicator for  y axis [Current prices, million euro]',
                style = {'font-size': '14px', 'text-align': 'left', 'color': colors['white']}
            ),
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],style={'width': '35%', 'float': 'right', 'display': 'inline-block', 'margin' : '10px 40px'})
    ]),
    html.Div([
        dcc.Graph(
            id='line-graphic2',
            style={"height" : 300, 'backgroundColor': colors['graphs']}
        ),
    ], style = {'margin' : '10px 20px'} 
    ),
     html.H1(
        children = 'Final Project Cloud Computing - Lena Becker - Master in Business Analytics ESADE Business School ',
        style = {'font-size': '14px', 'text-align': 'right', 'color': colors['white']}
        )
])

#Graph1
@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])

def update_graph1(xaxis_column_name1, yaxis_column_name1,
                 xaxis_type1, yaxis_type1,
                 year_value1):
    dff = df[df['TIME'] == year_value1]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name1]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name1]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name1]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'color': colors['linesdots'],
                'line': {'width': 0.5, 'color': colors['linesdots']}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name1,
                'type': 'linear' if xaxis_type1 == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name1 ,
                'type': 'linear' if yaxis_type1 == 'Linear' else 'log'
            },
            margin={'l': 60, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest',
            plot_bgcolor= colors['graphs'],
            paper_bgcolor= colors['background'],
            font= {
                'color': colors['white']
            }
        )
    }

#Country selection with clickData
@app.callback(
    dash.dependencies.Output('country','children'),
    [dash.dependencies.Input('indicator-graphic1','clickData')])

def update_clickdata(clickData):
    country_name = clickData['points'][0]['text']
    return ' {}'.format(country_name)


#Graph2
@app.callback(
    dash.dependencies.Output('line-graphic2', 'figure'),
    [dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('indicator-graphic1','clickData')])

def update_graph2(yaxis_column_name2, clickData):
    country2 = clickData['points'][0]['text']
    dff=df[df['GEO']== country2]
    
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_name2]['TIME'].values[:],
            y=dff[dff['NA_ITEM'] == yaxis_column_name2]['Value'],
            text=dff['TIME'].unique(), 
            mode='lines',
            line = dict(
                color = (colors['linesdots']),
                width = 4,),
            marker={
                'size': 15,
                'opacity': 1.0,
                'line': {'width': 0.5, 'color': colors['linesdots']}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'date'
            },
            yaxis={
                'title': yaxis_column_name2 + '\n',
                'type': 'log'
            },
            margin={'l': 60, 'b': 40, 't': 40, 'r':40},
            hovermode='closest',
            plot_bgcolor= colors['graphs'],
            paper_bgcolor= colors['background'],
            font= {
                'color': colors['white']
            }
        )
    }

if __name__ == '__main__':
    app.run_server()
