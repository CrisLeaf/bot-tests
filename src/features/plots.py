import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
sns.set_style('darkgrid')
sns.set_palette('muted')

import plotly.graph_objects as go

def plot_last_btc_with_SMA(
    df: pd.DataFrame,
    time_col: str,
    position_col: str,
    close_col: str,
    sma50_col: str,
    sma200_col: str,
):    
    df = df[-24*4*30: ]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df[time_col], y=df[close_col], mode='lines', name='Close Price'))

    fig.add_trace(go.Scatter(x=df[time_col], y=df[sma50_col], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=df[time_col], y=df[sma200_col], mode='lines', name='SMA 200'))

    fig.add_trace(go.Scatter(
        x=df[df[position_col] == 1][time_col], 
        y=df[sma50_col][df[position_col] == 1], 
        mode='markers', name='Buy Signal', 
        marker=dict(color='green', size=20, symbol='triangle-up')
    ))

    fig.add_trace(go.Scatter(
        x=df[df[position_col] == -1][time_col], 
        y=df[sma50_col][df[position_col] == -1], 
        mode='markers', name='Sell Signal', 
        marker=dict(color='red', size=20, symbol='triangle-down')
    ))

    fig.update_layout(
        width=1200,
        height=600,
        xaxis_title='Date',
        yaxis_title='Price',
        plot_bgcolor='rgb(40, 40, 40, 100)',
        paper_bgcolor='rgb(40, 40, 40, 100)',
        font=dict(color='rgb(200, 200, 200, 100)'),
        xaxis=dict(
            showline=True,
            linecolor='rgb(200, 200, 200, 100)',
            linewidth=2,
            gridcolor='rgb(100, 100, 100, 100)',
            zerolinecolor='rgb(80, 80, 80, 100)'
        ),
        yaxis=dict(
            showline=True,
            linecolor='rgb(200, 200, 200, 100)',
            linewidth=2,
            gridcolor='rgb(100, 100, 100, 100)',
            zerolinecolor='rgb(80, 80, 80, 100)'
        )
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    
    return fig

def plot_last_btc_with_BB(
    df: pd.DataFrame,
    time_col: str,
    # position_col: str,
    open_col: str,
    high_col: str,
    low_col: str,
    close_col: str,
    bb_upper_col: str,
    bb_middle_col: str,
    bb_lower_col: str,
):
    df = df[-24*4: ]

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df[time_col], open=df[open_col], high=df[high_col], low=df[low_col], close=df[close_col], name='Candlestick'
    ))

    fig.add_trace(go.Scatter(
        x=df[time_col], y=df[bb_upper_col], mode='lines', name='Bollinger Upper',
        line=dict(dash='dash', color='rgb(200, 200, 200, 100)')
    ))

    fig.add_trace(go.Scatter(
        x=df[time_col], y=df[bb_lower_col], mode='lines', name='Bollinger Lower',
        line=dict(dash='dash', color='rgb(200, 200, 200, 100)')
    ))

    fig.add_trace(go.Scatter(
        x=df[time_col], y=df[bb_middle_col], mode='lines', name='SMA20',
        line=dict(color='rgb(200, 200, 100, 100)')
    ))

    fig.update_layout(
        width=1200,
        height=600,
        xaxis_title='Date',
        yaxis_title='Price',
        plot_bgcolor='rgb(40, 40, 40, 100)',
        paper_bgcolor='rgb(40, 40, 40, 100)',
        font=dict(color='rgb(200, 200, 200, 100)'),
        xaxis=dict(
            showline=True,
            linecolor='rgb(200, 200, 200, 100)',
            linewidth=2,
            gridcolor='rgb(100, 100, 100, 100)',
            zerolinecolor='rgb(80, 80, 80, 100)'
        ),
        yaxis=dict(
            showline=True,
            linecolor='rgb(200, 200, 200, 100)',
            linewidth=2,
            gridcolor='rgb(100, 100, 100, 100)',
            zerolinecolor='rgb(80, 80, 80, 100)'
        )
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    
    return fig