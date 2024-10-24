import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
sns.set_style('darkgrid')
sns.set_palette('muted')


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

