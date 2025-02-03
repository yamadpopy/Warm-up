# -*- coding: utf-8 -*-
import time
import pyautogui as pag


def brother_cnc_connect():
    pag.hotkey('ctrl','c')
    # brother 開くボタン クリック
    for i in range(20):
        pag.hotkey('shift','tab')
        time.sleep(1)
    pag.press('enter')
    time.sleep(1)
    # OK ボタン クリック
    pag.press('tab',presses=18)
    time.sleep(1)
    pag.press('enter')
    time.sleep(1)
    # CNC 自動接続 開始
    pag.hotkey('shift','b')
