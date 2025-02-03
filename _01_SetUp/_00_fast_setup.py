# -*- coding: utf-8 -*-
import os
from _01_SetUp._01_path_create import path_create
from _05_File._01_data_read import yaml_read
from _05_File._02_data_save import yaml_save
from _01_SetUp._02_ADC_setup import adc_setup

def fast_setup(self):
    # NASの「設定.yaml」ファイル確認
    nas_setting_file_check(self,'設定.yaml')
    # path設定
    path_create(self)
    # 空フォルダ作成
    create_empty_folder(self)
    # デバイスごとのADC設定
    adc_setup(self)

def nas_setting_file_check(self,file_name):
    nas_file_path = os.path.join(
        self.dic['NASベースパス'],
        self.dic['プロジェクト名'],
        file_name
        )
    # NASに設定ファイルがあるか
    if os.path.exists(nas_file_path):
        # すでに存在している
        nas_dic = yaml_read(nas_file_path)
        if nas_dic != self.dic['データ構成']:
            # NASにある設定ファイルと異なる時は保存
            yaml_save(nas_file_path, self.dic['データ構成'])
            self.logger.info(f"NASにある設定ファイルと異なる")
        else:
            self.logger.info(f"NASにある設定ファイルと同じ")
    else:
        try:
            self.logger.info(f"NASに設定ファイルがないので保存")
            yaml_save(nas_file_path, self.dic['データ構成'])
        except:
            self.logger.error(f"NASに設定ファイルを保存できなかった")

def create_empty_folder(self):
    skip_list = [
        "ADC_exeパス",
        "ADC_iniパス",
        "ADC_portファイルパス",
        "machine_id",
        "device_type",
        ]
    for d0 in self.dic['データ構成'].values():
        for d1 in d0['デバイス'].values():
            for device_id in d1.keys():
                for k,v in self.now_dic[device_id].items():
                    if k not in skip_list:
                        try:
                            os.makedirs(v,exist_ok=True)
                        except:
                            self.logger.error(f"フォルダ作成できなかった。　{v}")
