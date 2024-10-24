import pandas as pd


def calculate_sma_columns(
    df: pd.DataFrame,
    windows: list[int],
):
    for window in windows:
        df[f'SMA{str(window)}'] = df['close'].rolling(window=window).mean()
    
    return df