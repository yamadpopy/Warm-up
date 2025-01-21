# -*- coding: utf-8 -*-
#2重起動防止
import os
import sys
import pywintypes
import win32api
import win32event
import winerror
UNIQUE_MUTEX_NAME = 'Global\\b-lex_2024-11'
handle = win32event.CreateMutex(None, pywintypes.FALSE, UNIQUE_MUTEX_NAME)
if not handle or win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(-1)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import threading
import time
import datetime
from pprint import pprint as pp

from _02_dic._02_setting_data_get import setting_data_get
from _09_ADC._00_adc_Initial_settings import adc_preferences
from _09_ADC._03_adc_start import adc_start_check,retry_ip
from _07_COM._01_com_data_get import com_settings
from _05_File._03_adc_row_data import row_data_check
from _09_ADC._05_kill_process import kill_process

class Main():
    def __init__(self, **kwargs):
        super(Main,self).__init__(**kwargs)
        # 設定情報読込
        self.dic = setting_data_get()
        # 起動中のADCすべて終了
        kill_process("AdvancedControl.exe")
        # ADC環境check
        adc_preferences(self)
        #pp(self.dic['データ構成'])
        self.ip_connect = []
        self.com_connect = []
        self.stop_event = threading.Event()  # 終了イベント

        # 順次ADC起動
        adc_start_check(self)

        # CNC通信確認
        if len(self.ip_connect) > 0:
            print('CNC通信確認')
            threading.Thread(target=retry_ip, args=(self,)).start()

        # RS232C信号受信確認
        if len(self.com_connect) > 0:
            print('RS232C信号受信確認')
            threading.Thread(target=com_settings, args=(self,)).start()

        # ADC生データフォルダ確認
        print('ADC生データフォルダ確認')
        threading.Thread(target=row_data_check, args=(self,)).start()

        # 時刻チェック
        print('時刻チェック')
        threading.Thread(target=self.check_time).start()

    def check_time(self):
        while not self.stop_event.is_set():
            current_time = datetime.datetime.now()
            # AM4:00を指定した時刻としてチェック
            if current_time.hour == 4 and current_time.minute == 0:
                print("AM4:00になりました。プログラムを終了します。")
                self.stop_event.set() # 終了イベントをセット
                break
            time.sleep(30) # 30秒ごとにチェック

if __name__ == "__main__":
    Main()
