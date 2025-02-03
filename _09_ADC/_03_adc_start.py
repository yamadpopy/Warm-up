# -*- coding: utf-8 -*-
import ctypes
import pyautogui as pag
from _06_LAN._01_ping import ping
from _08_cmd._02_adc_start import open_application_and_get_pid
from _09_ADC._04_adc_control import blex_connect
from _09_ADC._06_brother_cnc_connect import brother_cnc_connect

def adc_start_check(self):
    for device_id,d0 in self.now_dic.items():
        machine_id = d0["machine_id"]
        # CNC接続方式によって処理を分ける
        if self.dic['データ構成'][machine_id]['機械接続情報'].get('機械IP') == None:
            # CNC接続しない(RS232C接続)
            rs232c_start(self,device_id)
        else:
            # CNC接続する
            cnc_kid = self.dic['データ構成'][machine_id]['機械接続情報']['CNC種類']
            if "ファナック" == cnc_kid:
                fanuc_start(self,device_id)
            elif "ブラザー" == cnc_kid:
                brother_start(self,device_id)

def brother_start(self,device_id):
    # machine_id
    machine_id = self.now_dic[device_id]["machine_id"]
    # ip
    ip = self.dic['データ構成'][machine_id]['機械接続情報']['機械IP']
    # ping確認
    if ping(ip):
        # ADC起動
        adc_common_startup(self,device_id)
        # ブラザー独自のCNC通信設定
        brother_cnc_connect()
        # ADCウインドウ最小化
        ctypes.windll.user32.ShowWindow(self.now_dic[device_id]['hwnd'],6)
    else:
        print('ブラザーCNC通信切断状態')

def rs232c_start(self,device_id):
    # ADC起動
    adc_common_startup(self,device_id)
    # ADCウインドウ最小化
    ctypes.windll.user32.ShowWindow(self.now_dic[device_id]['hwnd'],6)

def fanuc_start(self,device_id):
    # ADC起動
    adc_common_startup(self,device_id)
    # shift+b CNC通信開始
    pag.hotkey('shift','t')
    # ADCウインドウ最小化
    ctypes.windll.user32.ShowWindow(self.now_dic[device_id]['hwnd'],6)

def adc_common_startup(self,device_id):
    # ADC起動
    hwnd = open_application_and_get_pid(self.now_dic[device_id]['ADC_exeパス'])
    self.now_dic[device_id]['hwnd'] = hwnd
    # b-lex測定開始
    blex_connect()
