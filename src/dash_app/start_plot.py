import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np


def create_start_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    df = pd.DataFrame({
        'x': np.random.rand(200),
        'y': np.random.rand(200),
        'label': np.random.choice(['Grupo A', 'Grupo B'], size=200)
    })

    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    app.layout = html.Div([
        html.H1('Gráfico de Dispersión Simple'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Grupo A', 'value': 'Grupo A'},
                {'label': 'Grupo B', 'value': 'Grupo B'}
            ],
            value='Grupo A'
        ),
        dcc.Graph(id='my-graph')
    ], className="container")

    @app.callback(Output('my-graph', 'figure'),
                  [Input('my-dropdown', 'value')])
    def update_graph(selected_label):
        dff = df[df['label'] == selected_label]
        
        figure = px.scatter(
            dff,
            x='x',
            y='y',
            title=f'Gráfico de Dispersión - {selected_label}',
            labels={'x': 'Eje X', 'y': 'Eje Y'}
        )
        return figure

    return app
