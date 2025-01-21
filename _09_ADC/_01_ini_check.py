# -*- coding: utf-8 -*-
import configparser
from configparser import ExtendedInterpolation
from _02_dic._01_settings_dic import ini_target

def ini_check(self,machine_id,device_type,device_id,tmp):
    adc_ini_path = self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ADCiniファイル']
    config_now = configparser.ConfigParser(interpolation=ExtendedInterpolation(),allow_no_value=True)
    config_now.optionxform = str
    config_now.read(adc_ini_path,encoding='cp932')
    for section,d in ini_target(self,machine_id,device_type,device_id,tmp).items():
        for key,val in d.items():
            config_now.set(section,key,str(val))
    # INIファイルに書き込む
    write_clean_ini(config_now,adc_ini_path)

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
