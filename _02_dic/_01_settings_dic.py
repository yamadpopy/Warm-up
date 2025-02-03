# -*- coding: utf-8 -*-

def cnc_settings(cnc_kind):
    dic = {
        "ファナック":{
            "cnc_kind_no":0,
            "processingindex":0,
            },
        "ブラザー":{
            "cnc_kind_no":1,
            "processingindex":29,
            },
        "三菱":{
            "cnc_kind_no":2,
            "processingindex":0,
            },
        "オークマ":{
            "cnc_kind_no":3,
            "processingindex":0,
            },
        "USB_CNC":{
            "cnc_kind_no":4,
            "processingindex":0,
            },
    }
    return dic[cnc_kind]

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

