import pandas as pd


def calculate_sma_columns(
    df: pd.DataFrame,
    windows: list[int],
):
    for window in windows:
        df[f'SMA{str(window)}'] = df['close'].rolling(window=window).mean()
    
    return df

def calculate_ema_columns(
    df: pd.DataFrame,
    windows: list[int],
):
    for window in windows:
        df[f'EMA{str(window)}'] = df['close'].ewm(span=window, adjust=False).mean()
    
    return df

def calculate_bollinger_bands(
    df: pd.DataFrame,
    windows: list[int],
):
    for window in windows:
        df[f'BB_Middle_{str(window)}'] = df['close'].rolling(window=window).mean()
        df[f'BB_Upper_{str(window)}'] = df[f'BB_Middle_{str(window)}'] + 2 * df['close'].rolling(window=window).std()
        df[f'BB_Lower_{str(window)}'] = df[f'BB_Middle_{str(window)}'] - 2 * df['close'].rolling(window=window).std()
    
    return df
