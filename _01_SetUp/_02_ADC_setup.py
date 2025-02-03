# -*- coding: utf-8 -*-
import os
import csv
import shutil
import configparser
from configparser import ExtendedInterpolation
from _02_dic._01_settings_dic import cnc_settings

def adc_setup(self):
    for machine_id,d0 in self.dic['データ構成'].items():
        for device_type,d1 in d0['デバイス'].items():
            for device_id in d1.keys():
                # ADC.exeファイルが存在するか
                adc_folder_path = self.now_dic[device_id]['ADCフォルダ']
                self.now_dic[device_id]['ADC_exeパス'] = os.path.join(adc_folder_path,'AdvancedControl.exe')
                self.now_dic[device_id]['ADC_tmpパス'] = os.path.join(adc_folder_path,'tmp')
                self.now_dic[device_id]['ADC_iniパス'] = os.path.join(adc_folder_path,'AdvancedControl.ini')
                self.now_dic[device_id]['ADC_portファイルパス'] = os.path.join(adc_folder_path,'COMPortNumber_MACAddress_ToolNumber_MIName.txt')
                if not os.path.exists(self.now_dic[device_id]['ADC_exeパス']):
                    # ADC.exefileが存在しないとき、ひな形ADCフォルダ内をADCフォルダにコピーする
                    shutil.copytree(r'.\settings\ひな形ADC',adc_folder_path,dirs_exist_ok=True)
                # AdvancedControl.iniが設定ファイル通りか
                ini_check(self,machine_id,device_type,device_id)
                # COMPortNumber_MACAddress_ToolNumber_MIName.txtが設定ファイル通りか
                adc_comport_check(self,machine_id,device_type,device_id)

def ini_check(self,machine_id,device_type,device_id):
    config_now = configparser.ConfigParser(
        interpolation=ExtendedInterpolation(),
        allow_no_value=True
        )
    config_now.optionxform = str
    config_now.read(self.now_dic[device_id]['ADC_iniパス'],encoding='cp932')
    for section,d in ini_target(self,machine_id,device_type,device_id).items():
        for key,val in d.items():
            config_now.set(section,key,str(val))
    # INIファイルに書き込む
    write_clean_ini(config_now,self.now_dic[device_id]['ADC_iniパス'])

# すべてのセクションとオプションを確認し、スペースを削除
def write_clean_ini(config, file_path):
    with open(file_path, 'w', encoding='cp932') as configfile:
        for section in config.sections():
            configfile.write(f'[{section}]\n')
            for key in config[section]:
                # スペースを削除
                clean_key = key.strip()
                clean_value = str(config[section][key]).strip()
                # イコールの前後のスペースも削除して書き込む
                configfile.write(f'{clean_key}={clean_value}\n')
            configfile.write('\n')  # セクション間に空行を追加

def ini_target(self,machine_id,device_type,device_id):
    # CNC接続しない設定
    dic = common_dic(self,machine_id,device_type,device_id)
    if self.dic['データ構成'][machine_id]['機械接続情報'].get('機械IP') != None:
        # CNC接続する設定に書き換え
        dic = cnc_yes(self,machine_id,dic)
    return dic

def adc_comport_check(self,machine_id,device_type,device_id):
    com_no = self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ポート番号']
    rows = []
    # ファイルを読み込み
    with open(self.now_dic[device_id]['ADC_portファイルパス'], mode='r', newline='',encoding='cp932') as infile:
        reader = csv.reader(infile, delimiter='\t')
        for row in reader:
            try:
                if row[0] == '9999':
                    row[0] = com_no
                if row[3] == 'test':  # MI名のtestを探す
                    row[3] = f"{device_type}_{device_id}"  # MI名をセンサー名に変更
            except:
                pass
            rows.append(row)  # 行をリストに追加
    # ファイルに書き込む
    with open(self.now_dic[device_id]['ADC_portファイルパス'], mode='w',encoding='cp932') as f:
        for row in rows:
            f.write("\t".join(map(str, row)) + "\n")

def common_dic(self,machine_id,device_type,device_id):
    # データ保存ファイルパス
    save_file = os.path.join(
        self.now_dic[device_id]['ローカル_生データフォルダ'],
        f"{device_type}_{device_id}.txt"
        )
    dic = {
        "GenericCNC":{
            "SGenericCncSavePathMiCncData":self.now_dic[device_id]['ローカル_生データフォルダ'],
            "SGenericCncSavePathOnMachineMeasurementResult":self.now_dic[device_id]['ADC_tmpパス'],
            "SGenericCncSavePathWorkOffset":self.now_dic[device_id]['ADC_tmpパス'],
            "SGenericCncSavePathToolOffset":self.now_dic[device_id]['ADC_tmpパス'],
            "SCncWorkNumberReadFilename":os.path.join(self.now_dic[device_id]['ADC_tmpパス'],'macro.txt'),
            "SGenericCncSavePathNcProgram":self.now_dic[device_id]['ADC_tmpパス'],
            "SGenericCncSavePathChangedToolNumber":self.now_dic[device_id]['ADC_tmpパス'],
            },
        "ComPortTransceiver":{
            "iComPortNumber":self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ポート番号'],
            },
        "Measurement":{
            "SMeasurementDataAppendSaveFilename":save_file,
            "SAMeasurementSetupAutomaticSaveAfterMeasurementSettingsFilename0":save_file,
            },
        "Dtw":{
            "SSettingsDtwDistanceFilename":os.path.join(self.now_dic[device_id]['ADC_tmpパス'],'DTW.txt'),
            },
    }
    return dic

def cnc_yes(self,machine_id,dic):
    items_list = [
        "BGenericCncDataCollectionMacroVariableValue",
        "BGenericCncDataCollectionMeasurementEndDataInitialize",
        "BGenericCncCommunication",
        ]
    for item in items_list:
        dic['GenericCNC'][item] = "TRUE"
    # CNCの種類
    cnc_kid = self.dic['データ構成'][machine_id]['機械接続情報']['CNC種類']
    dic['GenericCNC']['iGenericCncMacroVariableNumberProcessingIndex'] = cnc_settings(cnc_kid)['processingindex']
    dic['GenericCNC']['iGenericCncType'] = cnc_settings(cnc_kid)['cnc_kind_no']
    # CNC接続IP
    cnc_ip = self.dic['データ構成'][machine_id]['機械接続情報']['機械IP']
    if "ファナック" == cnc_kid:
        dic['GenericCNC']['SGenericCncFanucIpAddress'] = cnc_ip
    elif "ブラザー" == cnc_kid:
        dic['GenericCNC']['SGenericCncBrotherVisaAddress'] = f"TCPIP0::{cnc_ip}::10000::SOCKET"
    elif "三菱" == cnc_kid:
        dic['GenericCNC']['SGenericCncMitsubishiIpAddress'] = cnc_ip
    elif "オークマ" == cnc_kid:
        dic['GenericCNC']['SGenericCncOkumaIpAddress'] = cnc_ip

    # マクロ監視番号設定
    fast_no = self.dic['データ構成'][machine_id]['機械接続情報']['マクロ監視開始番号']
    item_list = [
        "iGenericCncMacroVariableNumberToolNumber",
        "iGenericCncMacroVariableNumberWorkNumber",
        "iGenericCncMacroVariableNumberTriggerMeasurementBeginEnd",
        "iGenericCncMacroVariableNumberTriggerRecordOnOff",
        "iGenericCncMacroVariableNumberTriggerReadOnMachineMeasurementResult",
        "iGenericCncMacroVariableNumberTriggerReadWorkOffset",
        "iGenericCncMacroVariableNumberTriggerReadToolOffset",
        "iGenericCncMacroVariableNumberOnMachineMeasurementResultFirstNumber",
        "iGenericCncMacroVariableNumberOnMachineMeasurementResultNumberOfData",
        "iGenericCncMacroVariableNumberWorkOffsetx",
        "iGenericCncMacroVariableNumberWorkOffsety",
        "iGenericCncMacroVariableNumberWorkOffsetz",
        "iGenericCncMacroVariableNumberToolOffsetLength",
        "iGenericCncMacroVariableNumberToolOffsetLengthWear",
        "iGenericCncMacroVariableNumberToolOffsetRadius",
        "iGenericCncMacroVariableNumberToolOffsetRadiusWear",
        "iGenericCncThresholdControlTriggerMacroVariableNumber",
        "iGenericCncMacroVariableNumberMitsubishiHead",
    ]
    for no,val in enumerate(item_list):
        count = fast_no + no
        dic['GenericCNC'][val] = count

    item_list = [
        "iSettingsDtwThresholdControlTriggerMacroVariableNumber",
        "iSettingsDtwThresholdControlOverThresholdMacroVariableNumber"
    ]
    for val in item_list:
        count += 1
        dic['Dtw'][val] = count

    item_list = [
        "iGenericCncMacroVariableNumberTriggerReadNcProgram",
        "iGenericCncMacroVariableNumberTriggerReadChangedToolNumber",
        "iGenericCncMacroVariableNumberGeneric"
    ]
    for val in item_list:
        count += 1
        dic['GenericCNC'][val] = count
    return dic

