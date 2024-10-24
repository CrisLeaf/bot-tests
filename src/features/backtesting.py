import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
sns.set_style('darkgrid')
sns.set_palette('muted')

import plotly.graph_objects as go


def get_profit_list(
    df: pd.DataFrame,
    position_col: str,
    close_col: str,
    investment_per_round: int,
    taker_fee: float = 0.004
) -> list:
    '''
    This function calculates the profit list for a given dataframe.
    
    Input
    -----
    df: pd.DataFrame
        The dataframe containing the data.
    position_col: str
        The column name containing the position values.
    close_col: str
        The column name containing the close values.
    investment_per_round: int
        The amount of money to invest in each round.
    taker_fee: float
        The taker fee to be applied.
        
    Output
    ------
    profits_list: list
        The list containing the profits for each round.
    '''
    idxs_tuples = []
    first_tuple = True

    for idx, pos in zip(df.index, df[position_col]):
        if pos == 1 and first_tuple:
            first_tuple = False
            idxs_tuples.append((idx, pos))
        elif pos == -1 and not first_tuple:
            first_tuple = True
            idxs_tuples.append((idx, pos))
            
    if len(idxs_tuples) % 2 != 0:
        idxs_tuples = idxs_tuples[:-1]
    
    profits_list = []

    for i in range(0, len(idxs_tuples), 2):
        id1, id2 = idxs_tuples[i][0], idxs_tuples[i+1][0]
        
        enter_price = df.iloc[id1][close_col]
        exit_price = df.iloc[id2][close_col] * (1-taker_fee)
        
        profit_percentage = (exit_price - enter_price) / enter_price
        
        total_profit = (1+profit_percentage) * investment_per_round * (1-taker_fee)
        
        profits_list.append(total_profit - investment_per_round)
    
    return profits_list

def plot_last_btc_with_signals(
    df: pd.DataFrame,
    time_col: str,
    position_col: str,
    close_col: str,
):    
    df = df.loc[df.shape[0] - 24*4*30: ]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df[time_col], y=df[close_col], mode='lines', name='Close Price'))

    fig.add_trace(go.Scatter(x=df[time_col], y=df['SMA50'], mode='lines', name='SMA50'))
    fig.add_trace(go.Scatter(x=df[time_col], y=df['SMA200'], mode='lines', name='SMA200'))

    fig.add_trace(go.Scatter(
        x=df[df[position_col] == 1][time_col], 
        y=df['SMA50'][df[position_col] == 1], 
        mode='markers', name='Buy Signal', 
        marker=dict(color='green', size=20, symbol='triangle-up')
    ))

    fig.add_trace(go.Scatter(
        x=df[df[position_col] == -1][time_col], 
        y=df['SMA50'][df[position_col] == -1], 
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
            gridcolor='rgb(200, 200, 200, 100)',
            zerolinecolor='rgb(200, 200, 200, 100)'
        ),
        yaxis=dict(
            showline=True,
            linecolor='rgb(200, 200, 200, 100)',
            linewidth=2,
            gridcolor='rgb(200, 200, 200, 100)',
            zerolinecolor='rgb(200, 200, 200, 100)'
        )
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    
    return fig