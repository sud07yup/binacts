import pandas as pd
import sqlite3
import re
from pprint import pprint as pp


# Read DB
def read_db(conn, table_name_list, start_time, end_time, candle_size, open_time, ma_list):
    cnt = 1
    all_dfs = []
    for table_name in table_name_list:
        
        print('_________________________________')
        print('')
        print(f'{cnt}: {table_name}')
        print('')
        
        # Construct the SQL SELECT statement with a WHERE clause
        sql = f'SELECT * FROM "{table_name}" WHERE timestamp BETWEEN ? AND ?'
        
        df = pd.read_sql_query(sql, conn, params=(start_time, end_time))
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp', inplace=False)
        dfs = resample_df(df, candle_size, open_time, ma_list)
        all_dfs.append(dfs)
        pp(dfs)
        
        cnt += 1
        
    return all_dfs

# Candle Resample
def resample_df(df, candle_size, open_time, ma_list):
    print('>>> Resample DataFrame')
    
    values = {
                'open': 'first', 
                'high': 'max', 
                'low': 'min', 
                'close': 'last', 
                'volume': 'sum', 
                'quote_asset_volume': 'sum', 
                'number_of_trades': 'sum', 
                'taker_buy_base_asset_volume': 'sum', 
                'taker_buy_quote_asset_volume': 'sum'
            }
    dfs = []
    period = f'{candle_size}H'
    if open_time == 'All':
        for o_time in range(24):
            start = f'{o_time}h' 
            df = df.resample(period, offset=start).agg(values)
            
            df = ma(df, 'close', ma_list)
            df = make_data(df)
            df = ma(df, 'noise', ma_list)
            dfs.append(df)
            
            
    else:
        start = f'{open_time}h' 
        df = df.resample(period, offset=start).agg(values)
        df = ma(df, 'close', ma_list)
        df = make_data(df)
        df = ma(df, 'noise', ma_list)
        dfs.append(df)
    
    # print(dfs)
    
    return dfs
        
def ma(df, row, ma_list):
    
    for period in ma_list:
        if period > 0:
            ma_name = f'{row}_ma_{period}'
            df[ma_name] = df[row].rolling(window=period).mean().round(decimals=3)
        else:
            pass
    
    return df

def make_data(df):
    df['noise'] = (1 - abs(df.open - df.close) / (df.high - df.low)).round(decimals=3)
    
    return df
    
def strategy(strategy):

    if strategy == '변동성돌파':
        print('변동성돌파 전략')
        # 변동성 자료 만들기 : (전고-전저) * k
        # 


def data_processing(df_list):
    print(df_list)