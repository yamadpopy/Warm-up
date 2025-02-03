# -*- coding: utf-8 -*-
import subprocess

def kill_process(process_name: str):
    # /f: 強制終了
    # /im: イメージ名による指定
    # エラー出力に "エラー" が含まれた場合にプロセスが存在していないとみなす例
    taskkill_cmd = ["taskkill", "/f", "/im", process_name]
    result = subprocess.run(taskkill_cmd, capture_output=True, text=True)
    if "エラー" in result.stderr:
        print(f"{process_name} は起動していません。")
    else:
        print(f"{process_name} を強制終了しました。")