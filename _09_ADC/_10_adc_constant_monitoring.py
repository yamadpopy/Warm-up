# -*- coding: utf-8 -*-
import ctypes
import threading
from _06_LAN._01_ping import ping
from _07_COM._02_serial_setup import serial_setup
from _09_ADC._03_adc_start import adc_common_startup

def adc_constant_monitoring(self):
    for device_id,d0 in self.now_dic.items():
        machine_id = d0["machine_id"]
        # CNC接続方式によって処理を分ける
        if self.dic['データ構成'][machine_id]['機械接続情報'].get('機械IP') == None:
            # CNC接続しない(RS232C接続)
            threading.Thread(target=rs232c_constant_monitoring, args=(self,device_id,)).start()
        else:
            # CNC接続する
            cnc_kid = self.dic['データ構成'][machine_id]['機械接続情報']['CNC種類']
            if "ブラザー" == cnc_kid:
                threading.Thread(target=brother_constant_monitoring, args=(self,device_id,)).start()

def rs232c_constant_monitoring(self,device_id):
    machine_id = self.now_dic[device_id]["machine_id"]
    flag = True
    # シリアル通信設定
    if self.dic['データ構成'][machine_id]['機械接続情報'].get('conprosysIP') != None:
        conprosysIP = self.dic['データ構成'][machine_id]['機械接続情報']['conprosysIP']
        if not ping(conprosysIP):
            flag = False
    com = self.dic['データ構成'][machine_id]['機械接続情報']['RS232Cポート番号']
    ser = serial_setup(com)
    if (ser != None) and flag:
        # シリアルモニタリング
        #serial_monitoring(ser)
        # ADC起動
        adc_common_startup(self,device_id)
        # ADCウインドウ最小化
        ctypes.windll.user32.ShowWindow(self.now_dic[device_id]['hwnd'],6)
    else:
        print('シリアル通信切断状態')

def brother_constant_monitoring(self,device_id):
    # machine_id
    machine_id = self.now_dic[device_id]["machine_id"]
    # ip
    ip = self.dic['データ構成'][machine_id]['機械接続情報']['機械IP']
    # ping確認
    if ping(ip):
        # ADC起動
        adc_common_startup(self,device_id)
        # ブラザー独自のCNC通信設定
        
        # ADCウインドウ最小化
        ctypes.windll.user32.ShowWindow(self.now_dic[device_id]['hwnd'],6)
    else:
        print('ブラザーCNC通信切断状態')