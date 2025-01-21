# -*- coding: utf-8 -*-
import subprocess

def kill_process(process_name: str):
    # tasklistコマンドで AdvancedControl.exe が実行中かをチェック
    tasklist_cmd = ["tasklist", "/FI", f"IMAGENAME eq {process_name}"]
    result = subprocess.run(tasklist_cmd, capture_output=True, text=True)

    # 実行結果をもとに、AdvancedControl.exe が実行中かを判定
    # 「INFO: No tasks are running...」などの文言がなければ起動している
    if "No tasks are running" not in result.stdout:
        print(f"{process_name} が起動しているため、強制終了します。")
        taskkill_cmd = ["taskkill", "/F", "/IM", f"{process_name}"]
        try:
            subprocess.run(taskkill_cmd, check=True)
            print(f"{process_name} を強制終了しました。")
        except subprocess.CalledProcessError as e:
            print("強制終了に失敗しました。:", e)
    else:
        # 実行中のプロセスが見つからない場合
        print(f"{process_name} は起動していません。強制終了を行いません。")