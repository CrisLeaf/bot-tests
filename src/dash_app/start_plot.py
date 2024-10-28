import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

def create_start_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    initial_data = pd.DataFrame(columns=['x', 'y', 'label'])

    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    app.layout = html.Div(
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'height': '95vh'
        },
        children=[
            dcc.Graph(
                id='my-graph',
                figure=generate_figure(initial_data, 0),
                style={'width': '50%', 'height': '50vh'},
                config={'displayModeBar': False},
            ),
            dcc.Interval(id='interval-component', interval=0.25*1000, n_intervals=0),
            dcc.Store(id='data-store', data=initial_data.to_dict('records'))
        ]
    )

    @app.callback(
        Output('my-graph', 'figure'),
        Output('data-store', 'data'),
        Input('interval-component', 'n_intervals'),
        State('data-store', 'data')
    )
    def update_graph(n, stored_data):
        df = pd.DataFrame(stored_data)

        if len(df) >= 25:
            df = df.iloc[0:0].copy()
        
        random_number = np.random.uniform(-1, 1) + len(df) / 5
        
        new_point = pd.DataFrame({
            'x': [len(df)],
            'y': [random_number],
            'label': [1 if random_number > 0 else -1]
        })
        df = pd.concat([df, new_point], ignore_index=True)

        figure = generate_figure(df, len(df))

        return figure, df.to_dict('records')

    return app

def generate_figure(df, x_right_range):
    fig = go.Figure()

    if len(df) > 0 and df['y'].iloc[0] > 0.4:
        fig.add_trace(go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines+markers',
            marker=dict(
                size=12,
                line=dict(width=2),
            ),
            line=dict(color='#1a1a18'),
        ))
    elif len(df) > 0 and df['y'].iloc[0] < 0.2:
        fig.add_trace(go.Bar(
            x=df['x'],
            y=df['y'],
            marker=dict(
                # color='blue',
                line=dict(width=2, color='#1a1a18')
            )
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='white'),
        ))
        

    fig.update_traces(
        marker_color=np.where(df['y'] >= 0, '#68ab5b', '#ec6058'),
        marker_line_color='#1a1a18',
        marker_line_width=2,
        hoverinfo='skip',
    )
    fig.update_layout(
        xaxis=dict(
            title_font=dict(size=14, color='rgba(0,0,0,0)'),
            tickfont=dict(color='rgba(0,0,0,0)'),
            gridcolor='rgba(0,0,0,0)',
            range=[-1, x_right_range],
            zeroline=False,
        ),
        yaxis=dict(
            title_font=dict(size=14, color='rgba(0,0,0,0)'),
            tickfont=dict(color='rgba(0,0,0,0)'),
            gridcolor='rgba(0,0,0,0)',
            zeroline=True,
            zerolinecolor='#1a1a18',
            zerolinewidth=2,
            range=[-1.1, 6.1]
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    
    return fig