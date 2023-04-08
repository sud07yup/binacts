import pandas as pd
import sqlite3
import re
import numpy as np
from pprint import pprint as pp

'''
values_list = [
0    values['start_time'], 
1    values['end_time'], 
2    values['candle_size'], 
3    values['open_time'],
4    values['ma_1'], 
5    values['ma_2'], 
6    values['ma_3'], 
7    values['ma_4'], 
8    values['ma_5'], 
9    values['ma_6'],
10    values['ma_score_1'], 
11    values['ma_score_2'], 
12    values['ma_score_3'], 
13    values['ma_score_4'], 
14    values['sep_cm1'], 
15    values['sep_cm2'], 
16    values['sep_cm3'], 
17    values['sep_cm4'],
18    values['sep_score_1'], 
19    values['sep_score_2'], 
20    values['sep_score_3'], 
21    values['sep_score_4'],
22    values['aggression'],
23    values['selected_noise']

]
'''


# Read DB
def read_db(conn, table_name_list, values_list, switch):
    cnt = 1
    all_dfs = []
    start_time = values_list[0]
    end_time = values_list[1]
    candle_size = values_list[2]
    open_time = values_list[3]
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
        dfs = resample_df(df, candle_size, open_time, values_list, switch)
        all_dfs.append(dfs)
        pp(dfs)
        
        cnt += 1
        
    return all_dfs


# Candle Resample
def resample_df(df, candle_size, open_time, values_list, switch):
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
            
            df = make_data(df, values_list, switch)
            
            dfs.append(df)
            
            
    else:
        start = f'{open_time}h' 
        df = df.resample(period, offset=start).agg(values)
        
        df = make_data(df, values_list, switch)
        
        dfs.append(df)
    
    # print(dfs)
    
    return dfs


def ma(df, row, ma_list):
    num = 1
    for period in ma_list: 
        if period == '':
            p = 0
        else:
            p = int(period)
        
        if p > 0:
            ma_name = f'{row}_ma_{num}'
            df[ma_name] = df[row].rolling(window=p).mean().round(decimals=3)
            num += 1
        else:
            pass
    
    return df


def make_data(df, values_list, switch):
    '''
    switch = [
        values['long_switch'], 
        values['short_switch'], 
        values['ma_switch'], 
        values['seperation_switch]
        values['system_noise'], 
        values['selected_noise]
        ]
    '''
    ma_list      = values_list[4:10]
    
    ma_s_1       = values_list[10]
    ma_s_2       = values_list[11]
    ma_s_3       = values_list[12]
    ma_s_4       = values_list[13]

    sep_base_cm1 = values_list[14]
    sep_base_cm2 = values_list[15]
    sep_base_cm3 = values_list[16]
    sep_base_cm4 = values_list[17]

    sep_score_1  = values_list[18]
    sep_score_2  = values_list[19]
    sep_score_3  = values_list[20]
    sep_score_4  = values_list[21] 

    aggression   = values_list[22]
    select_noise = values_list[23]

    long_switch        = switch[0]
    short_switch       = switch[1]
    ma_switch          = switch[2]
    seperation_switch  = switch[3]
    sys_noise_switch   = switch[4]
    sele_noise_switch  = switch[5]
        
    # base factors
    df['range'] = df.high - df.low
    df['noise'] = (1 - abs(df.open - df.close) / df.range).round(decimals=3)
    
    # 돌파 계수 설정
    df['l_break_ratio'] = df.noise * (1) # 전일 변동폭에 곱할 수: 노이즈에 뭘 곱할까? 고민 
    df['s_break_ratio'] = df.noise * (1)

    # 이평선 만들기
    df = ma(df, 'close', ma_list)
    df = ma(df, 'noise', ma_list)
    
    # 이격도
    seperation_cm1 = df.close.shift(1) / df.close_ma_1.shift(1) - 1
    seperation_cm2 = df.close.shift(1) / df.close_ma_2.shift(1) - 1
    seperation_cm3 = df.close.shift(1) / df.close_ma_3.shift(1) - 1
    seperation_cm4 = df.close.shift(1) / df.close_ma_4.shift(1) - 1


    ## 진입가격 설정
    if sele_noise_switch == 1 and sys_noise_switch == 0:
        df['l_target'] = df.open + df.range.shift(1) * select_noise
        df['s_target'] = df.open - df.range.shift(1) * select_noise

    else:
        df['l_target'] = df.open + df.range.shift(1) * df.l_break_ratio.shift(1)
        df['s_target'] = df.open - df.range.shift(1) * df.s_break_ratio.shift(1)

    ## 배팅비율
    # 이평선 스코어 
    score_sum = ma_s_1 + ma_s_2 + ma_s_3 + ma_s_4
    ma_1_long_score  = np.where(df.close_ma_1.shift(1) <= df.close.shift(1), ma_s_1, 0)
    ma_2_long_score  = np.where(df.close_ma_2.shift(1) <= df.close.shift(1), ma_s_2, 0)
    ma_3_long_score  = np.where(df.close_ma_3.shift(1) <= df.close.shift(1), ma_s_3, 0)
    ma_4_long_score  = np.where(df.close_ma_4.shift(1) <= df.close.shift(1), ma_s_4, 0)

    ma_1_short_score = np.where(df.close_ma_1.shift(1) >= df.close.shift(1), ma_s_1, 0)
    ma_2_short_score = np.where(df.close_ma_2.shift(1) >= df.close.shift(1), ma_s_2, 0)
    ma_3_short_score = np.where(df.close_ma_3.shift(1) >= df.close.shift(1), ma_s_3, 0)
    ma_4_short_score = np.where(df.close_ma_4.shift(1) >= df.close.shift(1), ma_s_4, 0)

    # 이격도 스코어  -  수정필요
    sep_1_long_score = np.where((seperation_cm1 <= float(sep_base_cm1)/100), sep_score_1, 0)
    sep_2_long_score = np.where((seperation_cm2 <= float(sep_base_cm2)/100), sep_score_2, 0)
    sep_3_long_score = np.where((seperation_cm3 <= float(sep_base_cm3)/100), sep_score_3, 0)
    sep_4_long_score = np.where((seperation_cm4 <= float(sep_base_cm4)/100), sep_score_4, 0)

    df['ss'] = sep_1_long_score


    long_bat_score_1    = (ma_1_long_score + ma_2_long_score + ma_3_long_score + ma_4_long_score) / score_sum
    short_bat_score_1   = (ma_1_short_score + ma_2_short_score + ma_3_short_score + ma_4_short_score) / score_sum

   

    
    # 실행 조건 
    long_con1 = np.where(df.close_ma_1.shift(1) <= df.close.shift(1), 1, 0)
    long_con2 = np.where(df.noise_ma_2.shift(1) >= df.noise.shift(1), 1, 0)
    long_con1 = np.where(df.close_ma_1.shift(1) <= df.close.shift(1), 1, 0)

    return df


def strategy(strategy):

    if strategy == '변동성돌파':
        print('변동성돌파 전략')
        # 변동성 자료 만들기 : (전고-전저) * k
        # 


def data_processing(df_list):
    print(df_list)








