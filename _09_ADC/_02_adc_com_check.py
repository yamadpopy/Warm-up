# -*- coding: utf-8 -*-
import csv


def adc_comport_check(self,machine_id,device_type,device_id):
    adc_txt_path = self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ADCportファイル']
    com_no = self.dic['データ構成'][machine_id]['デバイス'][device_type][device_id]['ポート番号']
    rows = []
    # ファイルを読み込み
    with open(adc_txt_path, mode='r', newline='',encoding='cp932') as infile:
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
    with open(adc_txt_path, mode='w',encoding='cp932') as f:
        for row in rows:
            f.write("\t".join(map(str, row)) + "\n")
