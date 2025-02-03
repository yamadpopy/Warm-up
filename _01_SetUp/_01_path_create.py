# -*- coding: utf-8 -*-
import os

def path_create(self):
    # path設定
    """
    デバイス番号:{
        ADCフォルダ:
        ローカル_生データフォルダ:
        ローカル_整理データフォルダ:
        ローカル_要約統計量:
        NAS_data:
        NAS_要約統計量:
    }
    """
    self.now_dic = {}
    for machine_id,d0 in self.dic['データ構成'].items():
        for device_type,d1 in d0['デバイス'].items():
            for device_id in d1.keys():
                self.now_dic[device_id] = {
                    'ADCフォルダ':os.path.abspath(os.path.join(
                        r"..\\",
                        self.dic['プロジェクト名'],
                        machine_id,device_type,device_id,"ADC"
                        )),
                    'ローカル_生データフォルダ':os.path.abspath(os.path.join(
                        r"..\\",
                        self.dic['プロジェクト名'],
                        machine_id,device_type,device_id,
                        "data"
                        )),
                    'ローカル_整理データフォルダ':os.path.abspath(os.path.join(
                        r"..\\",
                        self.dic['プロジェクト名'],
                        machine_id,device_type,device_id,
                        "result"
                        )),
                    'ローカル_要約統計量':os.path.abspath(os.path.join(
                        r"..\\",
                        self.dic['プロジェクト名'],
                        machine_id,device_type,device_id,
                        "result","要約統計量"
                        )),
                    'NAS_data':os.path.join(
                        self.dic['NASベースパス'],
                        self.dic['プロジェクト名'],
                        "data",machine_id,device_type,device_id,
                        "data"
                        ),
                    'NAS_要約統計量':os.path.join(
                        self.dic['NASベースパス'],
                        self.dic['プロジェクト名'],
                        "data",machine_id,device_type,device_id,
                        "要約統計量"
                        ),
                    'machine_id':machine_id,
                    'device_type':device_type,
                }
