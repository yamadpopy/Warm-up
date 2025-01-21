# -*- coding: utf-8 -*-
import pyautogui as pag
import time
import pyperclip

def blex_connect():
    # COMポート送受信機　ウィンドウ開く
    pag.hotkey('ctrl','t')
    time.sleep(1)
    # 開くボタン
    pag.press('tab',presses=6)
    pag.press('enter')
    # 測定終了ボタン
    pag.press('tab',presses=11)
    pag.press('enter',presses=3,interval=1.0)
    # データ消去ボタン
    for i in range(5):
        pag.hotkey('shift','tab')
    pag.press('enter')
    # リセットボタン
    for i in range(3):
        pag.hotkey('shift','tab')
    pag.press('enter',presses=5,interval=1.0)
    # データ表示（連続）ボタン
    pag.press('tab',presses=2)
    pag.press('space')
    # 受信データ　表示画面中に指定文字列があるか
    for i in range(3):
        pag.hotkey('shift','tab')
    target_str = 'ConnParms :: Interval=50000,SuperTout=6000000,SlaveLatency=0'
    while True:
        time.sleep(0.1)
        pag.hotkey('ctrl','a')
        pag.hotkey('ctrl','c')
        get_str = pyperclip.paste()
        # 行を取得し、空でない行のみをフィルタリング
        lines = [line for line in get_str.splitlines() if line.strip()]
        if target_str in get_str:
            judge = True
            break
        # 4行であるかどうかをチェック
        elif len(lines) == 4:
            # 各行の先頭が特定の文字列であることをチェック
            if (lines[0].startswith("Acc_x =") and
                lines[1].startswith("Acc_y =") and
                lines[2].startswith("Acc_z =") and
                lines[3].startswith("Δt =")):
                judge = False
                break
    if judge:
        normal_()
    else:
        finish_()

def finish_():
    # OK ボタン
    pag.press('tab',presses=14)
    pag.press('enter')

def normal_():
    # 測定間隔ボタン
    pag.press('tab',presses=10)
    pag.press('enter',interval=1.0)
    # 測定開始ボタン
    for i in range(2):
        pag.hotkey('shift','tab')
    pag.press('enter')
    # OK ボタン
    pag.press('tab',presses=6)
    pag.press('enter')
