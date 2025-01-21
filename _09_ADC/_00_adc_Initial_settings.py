# -*- coding: utf-8 -*-
import os
import shutil
from _02_dic._01_settings_dic import data_folder_key_folder,adc_key_fname
from _09_ADC._01_ini_check import ini_check
from _09_ADC._02_adc_com_check import adc_comport_check

def adc_preferences(self):
    # ADC環境check
    for machine_id,d0 in self.dic['データ構成'].items():
        for device_type,d1 in d0['デバイス'].items():
            for device_id in d1.keys():
                device_id_path = os.path.abspath(os.path.join(
                    r"..\\",
                    self.dic['プロジェクト名'],
                    machine_id,device_type,device_id
                ))

                # ローカルデータ保存場所
                for k,v in data_folder_key_folder().items():
                    path0 = os.path.join(device_id_path,v)
                    os.makedirs(path0,exist_ok=True)
                    self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id][k] = path0

                # NASデータ保存場所
                path0 = os.path.join(
                    self.dic['NASベースパス'],
                    self.dic['プロジェクト名'],
                    machine_id,device_type,device_id,
                    )
                self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['NAS'] = path0

                adc_folder_path = os.path.join(device_id_path,"ADC")
                os.makedirs(adc_folder_path,exist_ok=True)

                for k,v in adc_key_fname().items():
                    path0 = os.path.join(adc_folder_path,v)
                    self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id][k] = path0

                # ADC.exeファイルが存在するか
                adc_exe_path = self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ADC実行ファイル']
                if not os.path.exists(adc_exe_path):
                    # ADC.exefileが存在しないとき、ひな形ADCフォルダ内をADCフォルダにコピーする
                    shutil.copytree(r'.\settings\ひな形ADC',adc_folder_path,dirs_exist_ok=True)

                # AdvancedControl.iniが設定ファイル通りか
                ini_check(self,machine_id,device_type,device_id,os.path.join(adc_folder_path,"tmp"))

                # COMPortNumber_MACAddress_ToolNumber_MIName.txtが設定ファイル通りか
                adc_comport_check(self,machine_id,device_type,device_id)
