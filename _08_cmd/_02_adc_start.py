# -*- coding: utf-8 -*-
import subprocess
import time
import win32gui
import win32process
import os
import win32con


def open_application_and_get_pid(executable):
    """
    指定されたexeを起動し、そのPIDを取得する
    """
    # アプリケーションを指定したディレクトリで起動
    working_directory = os.path.dirname(executable)
    process = subprocess.Popen(executable, cwd=working_directory)
    # プロセスのPIDを返す
    hwnd = operate_on_application(process.pid)
    return hwnd

def get_window_handle(pid):
    """
    PIDからウィンドウハンドルを取得する
    """
    hwnds = []
    def callback(hwnd, param):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
    win32gui.EnumWindows(callback, None)
    # 一致するウィンドウハンドルがあれば返す
    return hwnds[0] if hwnds else None

def operate_on_application(pid):
    """
    PIDを指定してアプリケーションに対して操作を行う
    """
    signal = True
    while signal:
        try:
            hwnd = get_window_handle(pid)
            if hwnd != None:
                win32gui.ShowWindow(hwnd,win32con.SW_RESTORE) # SW_SHOW
                win32gui.SetForegroundWindow(hwnd) # フォアグラウンドにする
                #time.sleep(1) # ウィンドウがアクティブになるまで待機
                signal = False
        except:
            continue
    return hwnd



