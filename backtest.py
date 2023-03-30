import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import PySimpleGUI as sg
from re import T
import utility as uu
import ui
from pprint import pprint as pp

'''
2023_03_01 : 코인을 선택하거나 전체에 대해서 기간 선택해서 리샘플 하기 완료
2023_03_02 : 이평선 만드는 함수 추가
2023_03_14 : 전략 선택 콤보박스 추가
'''

class Backtest():
    def __init__(self):
        now_start = datetime.now()        
        # Define the timestamps you want to retrieve values between
                
        self.results = []
        
        # db에서 불러오기
        all_dfs = uu.read_db(conn, table_name_list, values_list, switch)
        
        # uu.data_processing(df_list)
        # self.results.append(df)
            
        now_end = datetime.now()
        
        timer = now_end - now_start
        msg = f'>>>  Timer : {timer}'    
        window['timer'].update(msg)    
    
        
    
    
            
if __name__== '__main__':
    # Connect to the database file
    conn = sqlite3.connect('C:\\coding\db\\binance_futures.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_name  = [row[0] for row in cursor.fetchall()]
    symbols     = [row[0][:-3] for row in cursor.fetchall()]


    # ui 
    ago = timedelta(days=30)
    # Create the PySimpleGUI window
    sg.set_options(font=('nanumgothic', 10))
        
    window = sg.Window('ACTS Backtest', ui.layout)
    
    while True:
        event, values = window.read()
                
        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Run Backtest':           
            strategy = values['_strategy_']

            values_list = [
                values['start_time'], values['end_time'], values['candle_size'], values['open_time'],
                values['ma_1'], values['ma_2'], values['ma_3'], values['ma_4'], values['ma_5'], values['ma_6'],
                values['ma_score_1'], values['ma_score_2'], values['ma_score_3'], values['ma_score_4'], 
                values['sep_cm1'], values['sep_m1m2'], values['sep_m2m3'], values['sep_m3m4'],
            ]
                        
            switch_val  = [
                values['long_switch'], values['short_switch'], 
                values['ma_switch'], values['noise_switch'], 
                values['seperation_switch'],
            ]
            
            switch = []
            for val in switch_val:
                if val == 'ON':
                    v = 1
                else:
                    v = 0
                switch.append(v)
            print(switch)
            if values['sym'] == True:
                # print(values['sym'])
                table_name_list = table_name
                
                 
            else:
                table_name_list = []
                symbol_list = [values['sym1'], values['sym2'], values['sym3'], 
                            values['sym4'], values['sym5'], values['sym6'],]
                for sym in symbol_list:
                    if sym != '':
                        s = f'{sym}USDT_1h'
                        table_name_list.append(s)
                    else:
                        pass
            
            
            Backtest()
                        
            # Backtest(start_time, end_time, candle_size, open_time)
            
            # backtest = Backtest(start_time, end_time)
            
            # for idx, result in enumerate(backtest.results):
            #     print(f'{idx + 1}: {table_name_list[idx]} --------------------')
            #     print(result)
            #     print()
    cursor.close()
    conn.close()
    window.close()
