
from datetime import datetime, timedelta
import PySimpleGUI as sg


candle_sizes = ['24', '12', '6', '4', '1']
open_times   = ['All', '0', '1', '2', '3', '4', '5', '6', '7', 
                '8', '9', '10', '11', '12', '13', '14', '15', 
                '16', '17', '18', '19', '20', '21', '22', '23']
    
ma_list         = list(range(0, 241))
score_list   = list(range(0, 100, 5))

switch_list = ['ON', 'OFF']


ago = timedelta(days=30)
# Create the PySimpleGUI window

sg.set_options(font=('nanumgothic', 10))

symbols_layout = [
    [sg.Checkbox('ALL', key='sym')],
    [sg.Text('1'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym1')], 
    [sg.Text('2'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym2')], 
    [sg.Text('3'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym3')], 
    [sg.Text('4'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym4')], 
    [sg.Text('5'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym5')], 
    [sg.Text('6'), sg.InputText(size=(5,3), font=('gothic', 10), key='sym6')]
]

# 이평선 선택
ma_layout = [
    [sg.Text('', font=('gothic', 9))],
    [sg.Text('1'), sg.Combo(values=ma_list, default_value=3, font=('gothic', 10), 
                            key='ma_1', enable_events=True)], 
    [sg.Text('2'), sg.Combo(values=ma_list, default_value=5, font=('gothic', 10), 
                            key='ma_2', enable_events=True)],
    [sg.Text('3'), sg.Combo(values=ma_list, default_value=10, font=('gothic', 10), 
                            key='ma_3', enable_events=True)],
    [sg.Text('4'), sg.Combo(values=ma_list, default_value=20, font=('gothic', 10), 
                            key='ma_4', enable_events=True)],
    [sg.Text('5'), sg.Combo(values=ma_list, default_value=60, font=('gothic', 10), 
                            key='ma_5', enable_events=True)],
    [sg.Text('6'), sg.Combo(values=ma_list, default_value=120, font=('gothic', 10), 
                            key='ma_6', enable_events=True)]
]

# 종가와 이평선들 사이의 대소관계에 따른 점수
ma_score_layout = [
    [sg.Text('MA_F', font=('gothic', 9)), sg.Combo(values=switch_list, default_value='ON', 
                            key='ma_switch', enable_events=True)],
    [sg.Text('1'), sg.Combo(values=score_list, default_value=60, font=('gothic', 10), 
                            key='ma_score_1', enable_events=True)],
    [sg.Text('2'), sg.Combo(values=score_list, default_value=30, font=('gothic', 10), 
                            key='ma_score_2', enable_events=True)],
    [sg.Text('3'), sg.Combo(values=score_list, default_value=5, font=('gothic', 10), 
                            key='ma_score_3', enable_events=True)],
    [sg.Text('4'), sg.Combo(values=score_list, default_value=5, font=('gothic', 10), 
                            key='ma_score_4', enable_events=True)], 
    [sg.Text('5'), sg.Combo(values=score_list, default_value=5, font=('gothic', 10), 
                            key='ma_score_4', enable_events=True)], 
    [sg.Text('6'), sg.Combo(values=score_list, default_value=5, font=('gothic', 10), 
                            key='ma_score_4', enable_events=True)],
]

# 이격도 종가와 각이평선들 사이 이격정도(%)
seperation_ratio_layout = [
    [sg.Text('seperation(%)', font=('gothic', 9))],
    [sg.Text('c/m1'), sg.Combo(values=score_list, default_value=5, font=('gothic', 10), 
                                key='sep_cm1', enable_events=True)],
    [sg.Text('c/m2'), sg.Combo(values=score_list, default_value=10, font=('gothic', 10), 
                                key='sep_cm2', enable_events=True)],
    [sg.Text('c/m3'), sg.Combo(values=score_list, default_value=20, font=('gothic', 10), 
                                key='sep_cm3', enable_events=True)],
    [sg.Text('c/m4'), sg.Combo(values=score_list, default_value=30, font=('gothic', 10), 
                                key='sep_cm4', enable_events=True)],
    [sg.Text('c/m5'), sg.Combo(values=score_list, default_value=40, font=('gothic', 10), 
                                key='sep_cm5', enable_events=True)],
    [sg.Text('c/m6'), sg.Combo(values=score_list, default_value=50, font=('gothic', 10), 
                                key='sep_cm6', enable_events=True)],
]

# 종가의 이격정도에 따른 점수
sep_score_layout = [
    [sg.Text('SEP_F', font=('gothic', 9)), sg.Combo(values=switch_list, default_value='ON', 
                            key='seperation_switch', enable_events=True)],
    [sg.Text('1'), sg.Combo(values=score_list, default_value=40, font=('gothic', 10), 
                            key='sep_score_1', enable_events=True)],
    [sg.Text('2'), sg.Combo(values=score_list, default_value=40, font=('gothic', 10), 
                            key='sep_score_2', enable_events=True)],
    [sg.Text('3'), sg.Combo(values=score_list, default_value=10, font=('gothic', 10), 
                            key='sep_score_3', enable_events=True)],
    [sg.Text('4'), sg.Combo(values=score_list, default_value=10, font=('gothic', 10), 
                            key='sep_score_4', enable_events=True)],
    [sg.Text('5'), sg.Combo(values=score_list, default_value=0, font=('gothic', 10), 
                            key='sep_score_4', enable_events=True)],
    [sg.Text('6'), sg.Combo(values=score_list, default_value=0, font=('gothic', 10), 
                            key='sep_score_4', enable_events=True)],
]

# filter_layout = [
#     [sg.Text('MA_F', font=()), sg.Combo(values=switch_list, default_value='ON', 
#                             key='ma_switch', enable_events=True),
#     sg.Text('NOISE_F'), sg.Combo(values=switch_list, default_value='ON', 
#                             key='noise_switch', enable_events=True),
#     sg.Text('SEPER_F'), sg.Combo(values=switch_list, default_value='ON', 
#                             key='seperation_switch', enable_events=True)],
# ]

date_layout = [
    [sg.Text('Start Date '), 
        sg.CalendarButton('Select', target='start_time', format='%Y-%m-%d 00:00:00'), 
        sg.InputText(default_text=(datetime.now()-ago).strftime('%Y-%m-%d 00:00:00'), 
                    key='start_time', size=(18, 1))],
    [sg.Text(' End Date '), 
        sg.CalendarButton('Select', target='end_time', format='%Y-%m-%d 00:00:00'),
        sg.InputText(default_text=datetime.now().strftime('%Y-%m-%d 00:00:00'), 
                    key='end_time', size=(18, 1))],
    [sg.Text('')],
    [sg.Text('Candle Size:'), 
        sg.Combo(values=candle_sizes, default_value=candle_sizes[0], 
                key='candle_size', enable_events=True),
        sg.Text('Open Time:'), 
        sg.Combo(values=open_times, default_value=open_times[0], 
                key='open_time', enable_events=True)]
]

strategy_list = ['변동성돌파_0', '변동성돌파_1', '변동성돌파_2']
strategy_layout = [
    [sg.Combo(values=strategy_list, size=(100,50), 
            key='_strategy_', enable_events=True)],
    [sg.Text('Long '), sg.Combo(values=switch_list, default_value='ON', 
                            key='long_switch', enable_events=True)],
    [sg.Text('Short'), sg.Combo(values=switch_list, default_value='OFF', 
                            key='short_switch', enable_events=True)],
]

layout = [
    [sg.Frame('Time Set', date_layout, element_justification='center', 
        title_color='yellow', size=(300,190)), 
    sg.Frame('Crypto Set', symbols_layout, element_justification='center', 
        title_color='yellow', size=(90,190)), 
    sg.Frame('MA Set', ma_layout, element_justification='right', 
        title_color='yellowgreen', size=(80,190)), 
    sg.Frame('MA Score', ma_score_layout, element_justification='right', 
        title_color='yellowgreen', size=(100,190)), 
    sg.Frame('Seperation', seperation_ratio_layout, element_justification='right', 
        title_color='darkgreen', size=(100,190)),
    sg.Frame('Sep Score', sep_score_layout, element_justification='right', 
        title_color='darkgreen', size=(100,190)),
    sg.Frame('Strategy', strategy_layout, element_justification='left', 
        title_color='yellowgreen', size=(180,190)),],
    [sg.Button('Run Backtest'), sg.Text('>>>  ', key='timer', font=('gothic', 12))],
    #[sg.Output(size=(200, 20))]
]
        
        