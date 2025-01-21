# -*- coding: utf-8 -*-
from pprint import pprint as pp
import serial
import threading
import win32gui
import win32con
import time
import pyautogui as pag
import ctypes


def com_settings(self):
    # {COMポート番号:[hwnd:000,]}
    result_dic = {}
    result_dic.keys
    for d0 in self.dic['データ構成'].values():
        if d0['機械接続情報']['RS232Cポート番号'] != None:
            for d1 in d0['デバイス'].values():
                for device_id in d1.keys():
                    for dic in self.com_connect:
                        if dic['device_id'] == device_id:
                            if result_dic.get(dic['RS232Cポート番号']) == None:
                                result_dic[dic['RS232Cポート番号']] = [dic['hwnd']]
                            else:
                                result_dic[dic['RS232Cポート番号']].append(dic['hwnd'])
    for com,hwnd_list in result_dic.items():
        threading.Thread(target=com_setting, args=(self,com,hwnd_list)).start()

def com_setting(self,com,hwnd_list):
    serial_para = serial.Serial(
                port=f'COM{com}',
                baudrate=19200,
                bytesize=8,
                parity= 'E',
                stopbits=2,
                rtscts=True,
                )
    while not self.stop_event.is_set():
        row = serial_para.readline()
        txt = clean_text(row)
        if txt == 'START':
            for hwnd in hwnd_list:
                window_01(hwnd,'b')
                ctypes.windll.user32.ShowWindow(hwnd,6) # ADCウインドウ最小化
        elif txt == 'END':
            for hwnd in hwnd_list:
                window_01(hwnd,'e')
                pag.hotkey('ctrl','d')
                time.sleep(0.5)
                pag.press('enter')
                ctypes.windll.user32.ShowWindow(hwnd,6) # ADCウインドウ最小化

def clean_text(data: bytes) -> str:
    """
    受信したバイト列をデコードし、
    改行・スペース・% を取り除いて返す。
    """
    text = data.decode('utf-8', errors='ignore')
    # 先頭・末尾の改行や空白は strip() で除去
    text = text.strip()
    # 文章中のスペースや % をさらに除去
    text = text.replace(' ', '').replace('%', '')
    return text

def window_01(hwnd,key):
    win32gui.ShowWindow(hwnd,win32con.SW_RESTORE) # SW_SHOW
    win32gui.SetForegroundWindow(hwnd) # フォアグラウンドにする
    time.sleep(1) # ウィンドウがアクティブになるまで待機
    pag.hotkey('ctrl',f"{key}")
