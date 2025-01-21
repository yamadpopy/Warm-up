# -*- coding: utf-8 -*-
import os
from _02_dic._00_settins_data import project_data
from _05_File._01_data_read import yaml_read
from _05_File._02_data_save import yaml_save

def setting_data_get():
    dic_project = project_data()
    # NASベースパスにアクセスできるか
    try:
        os.makedirs(dic_project['NASベースパス'],exist_ok=True)
    except:
        return dic_project

    print("起動時NAS接続可能")

    file_name = '設定.yaml'
    nas_file_path = os.path.join(dic_project['NASベースパス'],file_name)
    # NASに設定ファイルがあるか
    if os.path.exists(nas_file_path):
        # すでに存在している
        nas_dic = yaml_read(nas_file_path)
        if nas_dic != dic_project['データ構成']:
            # NASにある設定ファイルと異なる時は保存
            yaml_save(nas_file_path,dic_project['データ構成'])
    else:
        yaml_save(nas_file_path,dic_project['データ構成'])
    return dic_project