import pandas as pd
import requests
import json

r = requests.get('https://data.cityofnewyork.us/resource/uvpi-gqnh.json')
x = r.json()
df = pd.read_json(json.dumps(x))
df=pd.DataFrame(df)
df1 =  df[['tree_id' ,'health','spc_common', 'boroname']] # select columns

q1= df1.groupby(['boroname','spc_common', 'health'])['tree_id'].nunique().reset_index()

q1['proportion'] = q1.groupby(['boroname', 'spc_common']).transform(lambda x: 100*(x/x.sum()))


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.H2('NYC TREE HEALTH'),
    html.Label("Choose a Species"),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in q1.spc_common.unique()],
        value='American elm',
        style={'width':'50%'}
    ),
    html.Div(id='display-value'),
    dcc.Graph( id="output-graph"),
        
])

q1_1 = q1.loc[q1['health']=='Fair']
q1_2 = q1.loc[q1['health']=='Good']
q1_3 = q1.loc[q1['health']=='Poor']

@app.callback(dash.dependencies.Output('output-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
            
def update_value(value):

  #  test =test[test['spc_common']=='value']
    return({'data': [
        {'x': q1_1.boroname.unique(), 'y': q1_1.loc[q1_1['spc_common']==value].proportion, 'type': 'bar', 'name': u'Fair'},
        {'x': q1_2.boroname.unique(), 'y': q1_2.loc[q1_2['spc_common']==value].proportion, 'type': 'bar', 'name': u'Good'},
        {'x': q1_3.boroname.unique(), 'y': q1_3.loc[q1_3['spc_common']==value].proportion, 'type': 'bar', 'name': u'Poor'},
        ],
            'layout': {
                'title': 'Tree Health by Borough',
                'plot_bgcolor':colors['background'],
                'paper_bgcolor':colors['background'],
              
                'font': {
                    'color':colors['text']
                }
        }
           
    }
    )




def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server()
