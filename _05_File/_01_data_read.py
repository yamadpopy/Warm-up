# -*- coding: utf-8 -*-
import yaml
import pandas as pd
import numpy as np

from _02_dic._01_settings_dic import df_use_cols

def yaml_read(path1):
    with open(path1,encoding='utf-8') as f:
        dic = yaml.safe_load(f)
    return dic

def mi_row_data_read(row_f_path):
    df = pd.read_table(
        row_f_path,
        skiprows=14,
        header=0,
        usecols=list(df_use_cols().keys()),
        )
    df.rename(columns=df_use_cols(), inplace=True)
    df.set_index(df.columns[0], inplace=True)  # 最初の列[Time]をindexへ設定
    # -9999.999 を np.nan に置き換える
    df.replace(-9999.999,np.nan, inplace=True)
    # すべての値が欠損値NaNである列を削除
    df.dropna(how='all', axis=1,inplace=True)
    return df

def pkl_read(path0):
    return pd.read_pickle(path0)