# -*- coding: utf-8 -*-
import os

from _01_SetUp._01_path_create import path_create
from _02_dic._00_settins_data import project_data
from _05_File._01_data_read import yaml_read
from _05_File._02_data_save import yaml_save
from _01_SetUp._02_ADC_setup import adc_setup

def fast_setup(self):
    # 設定情報読込
    self.dic = project_data()
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
    else:
        yaml_save(nas_file_path, self.dic['データ構成'])

def create_empty_folder(self):
    for d0 in self.dic['データ構成'].values():
        for d1 in d0['デバイス'].values():
            for device_id in d1.keys():
                for k,v in self.now_dic[device_id].items():
                    if "要約統計量" not in k:
                        os.makedirs(v,exist_ok=True)

