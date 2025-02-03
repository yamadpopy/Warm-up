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

#def adc_start(self,dic):
#    # ADC起動
#    hwnd = open_application_and_get_pid(dic["exe_path"])
#    # b-lex測定開始
#    blex_connect()
#    return hwnd
#
#def retry_ip(self):
#    while not self.stop_event.is_set():
#        for no,dic in enumerate(self.ip_connect):
#            time.sleep(1)
#            if ping(dic["ip"]):
#                # pingが通る
#                if not dic["起動中"]:
#                    # ADC起動
#                    hwnd = adc_start(self,dic)
#                    self.ip_connect[no]["hwnd"] = hwnd
#                    # ADCウインドウ最小化
#                    ctypes.windll.user32.ShowWindow(hwnd,6)
#                    self.ip_connect[no]["起動中"] = True
#            else:
#                # pingが通らない
#                exe_check = startup_confirmation(dic["exe_path"])
#                if exe_check[0]:
#                    # ADC起動中
#                    kill_process(exe_check[1])
#                    self.ip_connect[no]["hwnd"] = None
#                    self.ip_connect[no]["起動中"] = False

