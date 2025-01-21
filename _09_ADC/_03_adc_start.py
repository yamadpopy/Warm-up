# -*- coding: utf-8 -*-
from _08_cmd._02_adc_start import open_application_and_get_pid
from _09_ADC._04_adc_control import blex_connect
from _06_LAN._01_ping import ping
from _08_cmd._01_starting_up_exe_check import startup_confirmation,kill_process
import ctypes
import time

def adc_start_check(self):
    for machine_id,d0 in self.dic['データ構成'].items():
        for device_type,d1 in d0['デバイス'].items():
            for device_id,d2 in d1.items():
                # CNC接続する場合、pingが通るか
                dic = {
                    'ip':d0['機械接続情報']['機械IP'],
                    "exe_path":d2['ADC実行ファイル'],
                    "machine_id":machine_id,
                    "device_type":device_type,
                    "device_id":device_id,
                    "起動中":True
                }
                if d0['機械接続情報']["RS232Cポート番号"] != None:
                    # シリアル通信
                    hwnd = adc_start(self,dic)
                    ctypes.windll.user32.ShowWindow(hwnd,6) # ADCウインドウ最小化
                    dic['hwnd'] = hwnd
                    dic['RS232Cポート番号'] = d0['機械接続情報']["RS232Cポート番号"]
                    self.com_connect.append(dic)
                else:
                    # CNC通信
                    dic["起動中"] = False
                    self.ip_connect.append(dic)

def adc_start(self,dic):
    # ADC起動
    hwnd = open_application_and_get_pid(dic["exe_path"])
    # b-lex測定開始
    blex_connect()
    return hwnd

def retry_ip(self):
    while not self.stop_event.is_set():
        for no,dic in enumerate(self.ip_connect):
            time.sleep(1)
            if ping(dic["ip"]):
                # pingが通る
                if not dic["起動中"]:
                    # ADC起動
                    hwnd = adc_start(self,dic)
                    self.ip_connect[no]["hwnd"] = hwnd
                    # ADCウインドウ最小化
                    ctypes.windll.user32.ShowWindow(hwnd,6)
                    self.ip_connect[no]["起動中"] = True
            else:
                # pingが通らない
                exe_check = startup_confirmation(dic["exe_path"])
                if exe_check[0]:
                    # ADC起動中
                    kill_process(exe_check[1])
                    self.ip_connect[no]["hwnd"] = None
                    self.ip_connect[no]["起動中"] = False
