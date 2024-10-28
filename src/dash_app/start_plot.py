import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output


def create_start_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    df = generate_random_data()

    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    app.layout = html.Div([
        dcc.Graph(id='my-graph', figure=generate_figure(df)),
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
    ], className="container")

    @app.callback(
        Output('my-graph', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n):
        new_df = generate_random_data()
        return generate_figure(new_df)

    return app

def generate_random_data():
    return pd.DataFrame({
        'x': np.random.rand(200),
        'y': np.random.rand(200),
        'label': np.random.choice(['Grupo A', 'Grupo B'], size=200)
    })

def generate_figure(df):
    figure = px.scatter(
        df,
        x='x',
        y='y',
        color='label',
        title='Gráfico de Dispersión',
        labels={'x': 'Eje X', 'y': 'Eje Y'}
    )
    return figure