# -*- coding: utf-8 -*-
import serial
import os

def data_folder_key_folder():
    dic = {
        "生データ格納場所":"data",
        "整理データ格納場所":"result",
    }
    return dic

def adc_key_fname():
    dic = {
        "ADC実行ファイル":"AdvancedControl.exe",
        "ADCiniファイル":"AdvancedControl.ini",
        "ADCportファイル":"COMPortNumber_MACAddress_ToolNumber_MIName.txt"
    }
    return dic

def cnc_kind_no(cnc):
    dic = {
        "ファナック":0,
        "ブラザー":1,
        "三菱":2,
        "オークマ":3,
        "USB CNC":4,
    }
    return dic[cnc]

def processingindex(cnc):
    dic = {
        "ファナック":0,
        "ブラザー":29,
        "三菱":0,
        "オークマ":0,
        "USB CNC":0,
    }
    return dic[cnc]

def serial_settings(com_no):
    dic = {
        "port":f'COM{com_no}',
        "baudrate":4800,
        "bytesize":7,
        "parity": serial.PARITY_EVEN,
        "stopbits":2
    }
    return dic

def df_use_cols():
    return {
        "02_PC時間(0開始)[s]":'Time',
        "05_加速度(並進,x)[m/s^2]":'ACC_X',
        "06_加速度(回転,y)[rad,m/s^2]":'ACC_Y',
        "07_加速度z[m/s^2]":'ACC_Z',
        "15_電池電圧[V]":'Volt',
        "22_機械座標(1)[mm]or[deg.]":'Pos_X',
        "23_機械座標(2)[mm]or[deg.]":'Pos_Y',
        "24_機械座標(3)[mm]or[deg.]":'Pos_Z',
        "28_モータ負荷(主軸)":'Spindle',
        "29_モータ負荷(1)":'servo_X',
        "30_モータ負荷(2)":'servo_Y',
        "31_モータ負荷(3)":'servo_Z',
    }

def ini_target(self,machine_id,device_type,device_id,tmp):
    cnc_kind = self.dic['データ構成'][machine_id]['機械接続情報']['CNC種類']
    cnc_no = cnc_kind_no(cnc_kind)
    processing_index = processingindex(cnc_kind)
    machine_ip = self.dic['データ構成'][machine_id]['機械接続情報']['機械IP']
    nc_com_no = self.dic['データ構成'][machine_id]['機械接続情報']['RS232Cポート番号']
    cnc_connect = "True"
    if nc_com_no != None:
        machine_ip = ''
        cnc_connect = "False"
    save_file = os.path.join(
        self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]["生データ格納場所"],
        f"{device_type}_{device_id}.txt"
        )
    dic = {
        "PROF_KEY":{
            "Wnd_type":0,
            "Wnd_top":0,
            "Wnd_left":953,
            "Wnd_bottom":527,
            "Wnd_right":1927,
            },
        "SPEEDIO":{
            "SSpeedioCncVisaAddress":f"TCPIP0::{machine_ip}::10000::SOCKET",
            },
        "GenericCNC":{
            "BGenericCncCommunication":cnc_connect,
            "iGenericCncType":cnc_no,
            "iGenericCncMacroVariableNumberProcessingIndex":processing_index,
            "SGenericCncFanucIpAddress":machine_ip,
            "SGenericCncBrotherVisaAddress":f"TCPIP0::{machine_ip}::10000::SOCKET",
            "SGenericCncSavePathMiCncData":tmp+r'\\',
            "SGenericCncSavePathOnMachineMeasurementResult":tmp+r'\\',
            "SGenericCncSavePathWorkOffset":tmp+r'\\',
            "SGenericCncSavePathToolOffset":tmp+r'\\',
            "SCncWorkNumberReadFilename":os.path.join(tmp,'macro.txt'),
            "SGenericCncSavePathNcProgram":tmp+r'\\',
            "SGenericCncSavePathChangedToolNumber":tmp+r'\\',
            "SGenericCncMitsubishiIpAddress":machine_ip,
            "SGenericCncOkumaIpAddress":machine_ip,
            },
        "ComPortTransceiver":{
            "iComPortNumber":self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ポート番号'],
            "iComPortSendTimeOut":50,
            "iComPortReceiveTimeOut":50,
            "iComPortBaudRate":1000000,
            "iPeripheralMeasurementInterval":5,
            },
        "Measurement":{
            "iMeasurementWait":2,
            "iUpdateViewFrequency":100,
            "dMeasurementStopTimerTime":3600.000000,
            "iNofDataToBeMeasured":1000000,
            "BMeasurementSetupLoopMeasurement":"FALSE",
            "iNumberOfTimesSendWirelessCommand":6,
            "iMeasurementDataSave":2,
            "SMeasurementDataAppendSaveFilename":save_file,
            "BMeasurementSetupAutomaticSaveAfterMeasurementInitializeMeasurementData":"FALSE",
            "iMeasurementSetupForcePeakHoldNumberOfData":10,
            "iMeasurementSetupAutomaticSaveAfterMeasurementSettingsNumber":1,
            "iMeasurementSetupAutomaticSaveAfterMeasurementNumberOfSettings":1,
            "iMeasurementSetupAutomaticSaveAfterMeasurementNumberOfSettings0":50,
            "iMeasurementSetupAutomaticSaveAfterMeasurementNumberOfSettings1":50,
            "iMeasurementSetupAutomaticSaveAfterMeasurementNumberOfSettings2":50,
            "SAMeasurementSetupAutomaticSaveAfterMeasurementSettingsSite0":"MachineTool_0",
            "SAMeasurementSetupAutomaticSaveAfterMeasurementSettingsFilename0":save_file,
            },
        "Graph":{
            "iTimeScale":0,
            "iNofPlotPoint":1000,
            "iAdcScale":0,
            "iMotorLoadScale":0,
            },
        "Maintenance":{
            "iPosition":1,
            "BShowMaintenanceInformation":"FALSE",
            "BShowProcessingConditions":"FALSE",
            },
        "Dtw":{
            "iSettingsDtwDistanceSetFullPath":0,
            "SSettingsDtwDistanceFilename":os.path.join(tmp,'DTW.txt'),
            },
        "ClosingDlg":{
            "iClosingDlgPositionLeft":1440,
            "iClosingDlgPositionTop":263,
            },
        "ClosingMessage":{
            "iiCloseMessageDlgPositionLeft":1440,
            "iiCloseMessageDlgPositionTop":263,
            },
    }
    return dic

