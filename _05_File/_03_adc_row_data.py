# -*- coding: utf-8 -*-
import os
import shutil
import datetime
import time
import pandas as pd
from _05_File._01_data_read import mi_row_data_read,pkl_read

def row_data_check(self):
    while not self.stop_event.is_set():
        time.sleep(1)
        for d0 in self.dic['データ構成'].values():
            for d1 in d0['デバイス'].values():
                for d2 in d1.values():
                    row_folder_path = d2['生データ格納場所']
                    result_folder_path = d2['整理データ格納場所']
                    nas_folder_path = d2['NAS']
                    time.sleep(1)
                    row_folder_check(row_folder_path,result_folder_path)
                # NASへ保存
                result_folder_check(nas_folder_path,result_folder_path)

def row_folder_check(row_folder_path,result_folder_path):
    for row_f in os.listdir(row_folder_path):
        # ファイルが書き込み中かどうかを判定
        row_f_path = os.path.join(row_folder_path,row_f)
        if is_file_locked(row_f_path):
            continue
        # dfへ読込
        df = mi_row_data_read(row_f_path)
        # 有効なデータか判断
        if data_judge(df):
            # 有効データではないので削除
            try:
                os.remove(row_f_path)
            except:
                continue
        # ファイル名からyyyy-mm取得
        year_month,date_time_obj = get_day(row_f)
        # ローカルのresultフォルダへgz拡張子で保存
        save_folder = os.path.join(result_folder_path,'data',year_month)
        os.makedirs(save_folder,exist_ok=True)
        #save_file_name = f"{row_f[:-3]}gz"
        save_file_name = f"{row_f[:-3]}csv"
        df.to_csv(
            os.path.join(save_folder,save_file_name),
            index=False,
            #compression='gzip'
            )
        # 統計量保存
        describe_check(result_folder_path,df,date_time_obj,year_month,save_file_name)
        # 処理を終えたので、生データは削除
        try:
            os.remove(row_f_path)
        except:
            continue

def describe_check(result_folder_path,df_row,date_time_obj,year_month,save_file_name):
    df_des = df_row.describe()
    pkl_path = os.path.join(result_folder_path,'要約統計量.pkl')
    csv_path = os.path.join(result_folder_path,'要約統計量.csv')
    df_now = first_create(df_row,df_des,date_time_obj,year_month,save_file_name)
    if os.path.exists(pkl_path):
        df_old = pkl_read(pkl_path)
        # df_nowのうちdf_oldに存在しないインデックスの行を選択
        df_now = df_now[~df_now.index.isin(df_old.index)]
        save_df = pd.concat([df_old,df_now])
        save_df.sort_index(inplace=True)
    else:
        save_df = df_now
    save_df.to_pickle(pkl_path)
    save_df.to_csv(csv_path)

def first_create(df_row,df_des,date_time_obj,year_month,save_file_name):
    d = {
        'create_time':date_time_obj,
        'Time_max':df_row.index.max()
        }
    for col in df_des.columns.values:
        for row in df_des.index.values:
            if row != 'count':
                d[f"{col}_{row}"] = [round(df_des.at[row,col],5)]
    d['year_month'] = year_month
    d['file_name'] = save_file_name
    df = pd.DataFrame(d)
    df.set_index('create_time', inplace=True)
    return df

def result_folder_check(path_nas,path_local):
    # NASへ保存
    # path_local以下の全てのファイルとディレクトリを取得
    for root, dirs, files in os.walk(path_local):
        # 相対パスを取得
        relative_path = os.path.relpath(root, path_local)
        target_nas_dir = os.path.join(path_nas, relative_path)
        # NASに同じディレクトリが存在しない場合は作成
        if not os.path.exists(target_nas_dir):
            os.makedirs(target_nas_dir,exist_ok=True)
        # ファイルを処理
        for file in files:
            local_file_path = os.path.join(root, file)
            nas_file_path = os.path.join(target_nas_dir, file)
            # NASにファイルが存在しない場合はコピー
            if not os.path.exists(nas_file_path):
                shutil.copy2(local_file_path, nas_file_path)
                print(f"Copied: {local_file_path} to {nas_file_path}")
            # サイズを確認
            if os.path.getsize(local_file_path) == os.path.getsize(nas_file_path):
                print(f"Size match for: {nas_file_path}")
                # コピー元を削除
                os.remove(local_file_path)
                print(f"Deleted original: {local_file_path}")
            else:
                print(f"Size mismatch for: {nas_file_path}, original not deleted.")

def get_day(filename):
    # ファイル名から日付と時間を抽出
    # 最初に拡張子を除去し、アンダースコアで分割
    base_name = filename.split('.')[0]
    parts = base_name.split('_')
    # 日付と時間の部分を抽出
    date_str = parts[2]  # '20241204'
    time_str = parts[3]  # '133214805'
    # yyyy-mm 形式の取得
    year_month = f"{date_str[:4]}-{date_str[4:6]}"  # '2024-12'
    # datetime オブジェクトの作成
    date_time_str = f"{date_str} {time_str[:6]}"  # '2024-12-04 13:32:14'
    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y%m%d %H%M%S")
    return year_month,date_time_obj

def data_judge(df):
    if df.empty: # dfが空ではないか
        return True
    if df.index.max() < 60.0: # 測定時間が1分以上か
        return True

def is_file_locked(filepath):
    # 一時的にファイルを開いて書き込めるかどうかを確認
    try:
        with open(filepath, 'a'):
            return False  # 書き込めるので、ロックされていない
    except IOError as e:
        return True  # IOErrorが発生した場合、他のアプリがロックしている可能性が高い
