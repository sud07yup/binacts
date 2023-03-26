import pandas as pd
import sqlite3
import re
from pprint import pprint as pp


# Read DB
def read_db(conn, table_name_list, start_time, end_time, candle_size, open_time, ma_list, switch):
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
        dfs = resample_df(df, candle_size, open_time, ma_list, switch)
        all_dfs.append(dfs)
        pp(dfs)
        
        cnt += 1
        
    return all_dfs


# Candle Resample
def resample_df(df, candle_size, open_time, ma_list, switch):
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
            
            
            df = make_data(df, ma_list, switch)
            
            dfs.append(df)
            
            
    else:
        start = f'{open_time}h' 
        df = df.resample(period, offset=start).agg(values)
        
        df = make_data(df, ma_list, switch)
        
        dfs.append(df)
    
    # print(dfs)
    
    return dfs


def ma(df, row, ma_list):
    
    for period in ma_list: 
        if period == '':
            p = 0
        else:
            p = int(period)
        
        if p > 0:
            ma_name = f'{row}_ma_{p}'
            df[ma_name] = df[row].rolling(window=p).mean().round(decimals=3)
        else:
            pass
    
    return df


def make_data(df, ma_list, switch):
    # base factors

    
    df['range'] = df.high - df.low
    df['noise'] = (1 - abs(df.open - df.close) / df.range).round(decimals=3)
    
    df['l_break_ratio'] = df.noise * (1) # 전일 변동폭에 곱할 수: 노이즈에 뭘 곱할까? 고민 
    df['s_break_ratio'] = df.noise * (1)

    df = ma(df, 'close', ma_list)
    df = ma(df, 'noise', ma_list)
       
    df['l_target'] = df.open + df.range.shift(1) * df.l_break_ratio.shift(1)
    df['s_target'] = df.open - df.range.shift(1) * df.s_break_ratio.shift(1)

    df = df[['range', 'l_break_ratio', 'l_target', 's_break_ratio', 's_target']]

    return df


def strategy(strategy):

    if strategy == '변동성돌파':
        print('변동성돌파 전략')
        # 변동성 자료 만들기 : (전고-전저) * k
        # 


def data_processing(df_list):
    print(df_list)








