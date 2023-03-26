import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import PySimpleGUI as sg
from re import T
import util.utility as uu
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
        self.start_time = start_time
        self.end_time   = end_time
        
        self.results = []
        
        # db에서 불러오기
        all_dfs = uu.read_db(conn, table_name_list, start_time, end_time, candle_size, open_time, ma_list, switch)
        
        # uu.data_processing(df_list)
        # self.results.append(df)
            
        now_end = datetime.now()
        
        timer = now_end - now_start
        msg = f'>>>  Timer : {timer}'    
        window['timer'].update(msg)    
    
        
    
    
            
if __name__== '__main__':
    # Connect to the database file
    conn = sqlite3.connect('D:\\db\\binance_futures.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_name  = [row[0] for row in cursor.fetchall()]
    symbols     = [row[0][:-3] for row in cursor.fetchall()]
    
    
    
    
    candle_sizes = ['24', '12', '6', '4', '1']
    open_times   = ['All', '0', '1', '2', '3', '4', '5', '6', '7', 
                    '8', '9', '10', '11', '12', '13', '14', '15', 
                    '16', '17', '18', '19', '20', '21', '22', '23']
        
    ma_list         = list(range(0, 241))
    ma_score_list   = list(range(0, 100, 5))
    
    switch_list = ['ON', 'OFF']
    
    
    ago = timedelta(days=30)
    # Create the PySimpleGUI window
    
    sg.set_options(font=('nanumgothic', 10))
    
    symbols_layout = [
        [sg.Checkbox('ALL CRYPTOS', key='sym')],
        [sg.Text('1'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym1'), 
        sg.Text('2'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym2'),], 
        [sg.Text('3'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym3'), 
        sg.Text('4'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym4'),], 
        [sg.Text('5'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym5'), 
        sg.Text('6'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym6'),]
    ]
    
    ma_layout = [
        [sg.Text('Select MA')], 
        [sg.Text('1'), sg.Combo(values=ma_list, default_value=3, font=('gothic', 10), key='ma_1', enable_events=True), 
        sg.Text('2'), sg.Combo(values=ma_list, default_value=5, font=('gothic', 10), key='ma_2', enable_events=True),],
        [sg.Text('3'), sg.Combo(values=ma_list, default_value=10, font=('gothic', 10), key='ma_3', enable_events=True),
        sg.Text('4'), sg.Combo(values=ma_list, default_value=20, font=('gothic', 10), key='ma_4', enable_events=True),],
        [sg.Text('5'), sg.Combo(values=ma_list, default_value=60, font=('gothic', 10), key='ma_5', enable_events=True),
        sg.Text('6'), sg.Combo(values=ma_list, default_value=120, font=('gothic', 10), key='ma_6', enable_events=True)]
    ]
    
    ma_score_layout = [
        [sg.Text('1'), sg.Combo(values=ma_score_list, default_value=60, font=('gothic', 10), key='ma_score_1', enable_events=True)],
        [sg.Text('2'), sg.Combo(values=ma_score_list, default_value=30, font=('gothic', 10), key='ma_score_2', enable_events=True)],
        [sg.Text('3'), sg.Combo(values=ma_score_list, default_value=5, font=('gothic', 10), key='ma_score_3', enable_events=True)],
        [sg.Text('4'), sg.Combo(values=ma_score_list, default_value=5, font=('gothic', 10), key='ma_score_4', enable_events=True)],
    ]
    
    
    filter_layout = [
        [sg.Text('MA_F'), sg.Combo(values=switch_list, default_value='ON', key='ma_switch', enable_events=True),
        sg.Text('NOISE_F'), sg.Combo(values=switch_list, default_value='ON', key='noise_switch', enable_events=True)],
    ]
    
    date_layout = [
        [sg.Text('Start Date '), 
            sg.CalendarButton('Select', target='start_time', format='%Y-%m-%d 00:00:00'), 
            sg.InputText(default_text=(datetime.now()-ago).strftime('%Y-%m-%d 00:00:00'), 
                        key='start_time', size=(18, 1))],
        [sg.Text(' End Date '), 
            sg.CalendarButton('Select', target='end_time', format='%Y-%m-%d 00:00:00'),
            sg.InputText(default_text=datetime.now().strftime('%Y-%m-%d 00:00:00'), 
                        key='end_time', size=(18, 1))],
        [sg.Text('Candle Size:'), 
            sg.Combo(values=candle_sizes, default_value=candle_sizes[0], 
                    key='candle_size', enable_events=True),
            sg.Text('Open Time:'), 
            sg.Combo(values=open_times, default_value=open_times[0], 
                    key='open_time', enable_events=True)]
    ]
    
    strategy_list = ['변동성돌파_0', '변동성돌파_1', '변동성돌파_2']
    strategy_layout = [
        [sg.Combo(values=strategy_list, size=(100,50), key='_strategy_', enable_events=True)],
        [sg.Text('Long '), sg.Combo(values=switch_list, default_value='ON', key='long_switch', enable_events=True)],
        [sg.Text('Short'), sg.Combo(values=switch_list, default_value='OFF', key='short_switch', enable_events=True)],
    ]
    
    layout = [
        [   sg.Frame('Time Set', date_layout, element_justification='center', title_color='yellowgreen', size=(300,130)), 
            sg.Frame('Crypto Set', symbols_layout, element_justification='center', title_color='yellowgreen', size=(160,130)), 
            sg.Frame('MA Set', ma_layout, element_justification='center', title_color='yellowgreen', size=(170,130)), 
            sg.Frame('MA Score Set', ma_score_layout, element_justification='center', title_color='yellowgreen', size=(90,130)),
            sg.Frame('Strategy', strategy_layout, element_justification='left', title_color='yellowgreen', size=(180,130))],
        [sg.Frame('Filters', filter_layout, element_justification='left', title_color='darkorange', size=(600,50))],
        [sg.Button('Run Backtest'), sg.Text('>>>  ', key='timer', font=('gothic', 12))],
        #[sg.Output(size=(200, 20))]
    ]
    
    window = sg.Window('ACTS Backtest', layout)
    
    while True:
        event, values = window.read()
                
        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Run Backtest':
            start_time  = values['start_time']
            end_time    = values['end_time']
            candle_size = values['candle_size']
            open_time   = values['open_time']
            
            ma_list = [values['ma_1'], values['ma_2'], values['ma_3'], 
                        values['ma_4'], values['ma_5'], values['ma_6']]
            
            strategy = values['_strategy_']

            switch = [values['long_switch'], values['short_switch']]
            
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
