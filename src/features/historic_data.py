"""
This script connects to the Kraken API to retrieve historical cryptocurrency price data.

Features:
- Loads API credentials from a `kraken.key` file.
- Defines the `get_historic` function to obtain OHLC (Open, High, Low, Close) data for a specific cryptocurrency pair.
- Saves the retrieved historical data into a CSV file in the `data/raw/` folder.

Requirements:
- krakenex: library for interacting with the Kraken API.
- pandas: library for data manipulation and data structures.

Example Usage:
- Run the script to download historical data for Bitcoin (BTC) to USD (XXBTZUSD) at 15-minute intervals and save the results in a CSV file.
"""
import krakenex
import pandas as pd
import time

from datetime import datetime

import os


CONFIGS_PATH = 'configs/'
DATA_RAW_PATH = 'data/raw/'


api = krakenex.API()
api.load_key(CONFIGS_PATH + 'kraken.key')


def get_historic(pair, interval=1_440, since=None):
    parameters = {
        'pair': pair,
        'interval': interval
    }
    
    if since:
        if isinstance(since, str):
            since = int(datetime.strptime(since, '%Y-%m-%d').timestamp())
        parameters['since'] = since
    
    ohlc = api.query_public('OHLC', parameters)
    
    if 'error' in ohlc and ohlc['error']:
        raise Exception(f'Kraken API error: {ohlc["error"]}')
    
    data = ohlc['result'][list(ohlc['result'].keys())[0]]
    
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])

    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    return df

def concatenate_data(folder_path):
    file_names = os.listdir(folder_path)

    all_data = pd.DataFrame()

    for file_name in file_names:
        if file_name == 'all_data.pkl':
            continue
        
        data = pd.read_csv(folder_path + file_name)
        all_data = pd.concat([all_data, data], axis=0)
        
    all_data.drop_duplicates(subset='time', keep='first', inplace=True)
    all_data.reset_index(drop=True, inplace=True)
    all_data['time'] = pd.to_datetime(all_data['time'])
    
    all_data.to_pickle(folder_path + 'all_data.pkl')


if __name__ == '__main__':
    pair_btc_usd = 'XXBTZUSD'
    historic_data = get_historic(pair_btc_usd, interval=15, since=None)
    
    output_file_name = 'data' + '_' + \
    str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '_' + \
        str(datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second) + '.csv'
    
    historic_data.to_csv(DATA_RAW_PATH + 'historic_btc_15min_interval/' +  output_file_name, index=False)

    print('Historic data saved successfully!')
    
    folder_path = DATA_RAW_PATH + 'historic_btc_15min_interval/'    
    concatenate_data(folder_path)
    
    print('Data concatenated successfully!')