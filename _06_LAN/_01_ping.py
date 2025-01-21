# -*- coding: utf-8 -*-
import subprocess
import platform


def ping(ip):
    # オペレーティングシステムを確認し、pingコマンドに適した引数を用意
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    # subprocessを使ってpingコマンドを実行
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        # 出力内容をチェック
        if "バイト数" in output:
            # "通信状態: OK", "white", "#4CAF50"
            return True
        else:
            # "通信状態: NG", "white", "#F44336"
            return False
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # "通信状態: エラー", "black", "#FFEB3B"
        return False
