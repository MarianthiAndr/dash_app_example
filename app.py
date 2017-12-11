
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('nama_10_gdp_1_Data.csv')

available_indicators = df['UNIT'].unique()
df1 = df[df['UNIT'] == 'Current prices, million euro']

value= df['Value'].unique()

geo=df['GEO'].unique()

indicators = df['NA_ITEM'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Current prices, million euro'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Chain linked volumes (2010), million euro'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
       dcc.Graph(id='scatter'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
     html.Div([
        html.Div([
            dcc.Dropdown( id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in geo],
                value='Greece'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
        
         html.Div([
            dcc.Dropdown( 
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in indicators],
                value= "Gross domestic product at market prices"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
    dcc.Graph(id='linegraph'),
])

@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['UNIT'] == xaxis_column_name]['Value'],
            y=dff[dff['UNIT'] == yaxis_column_name]['Value'],
            text=dff[dff['UNIT'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={'color': 'red',
                'size': 17,
                'opacity': 0.5,
                'line': {'width': 0.8, 'color': 'white'}
            }
        )],
        'layout': go.Layout( title='Different Indicators',
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 150, 'b': 70, 't': 70, 'r': 100},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('linegraph', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    dff = df1[df1['GEO'] == yaxis_column_name]                      
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={ 'color': 'orange',
                'size': 15,
                'opacity': 1.5,
                'line': {'width': 1, 'color': 'black'}
            }
        )],
        'layout': go.Layout( title='Indicators for each country',
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 150, 'b': 70, 't': 70, 'r': 100},
            hovermode='closest'
        )
    }


if __name__ == '__main__': 
    app.run_server(debug=False) 

