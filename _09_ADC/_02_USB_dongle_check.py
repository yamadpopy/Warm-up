# -*- coding: utf-8 -*-
import time
import usb.core
import usb.util

def dongle_check(self):
    # USBドングルを認識しているか
    if not dongle_check(self):
        self.logger.error(f"ADC　USBドングル　認識なし")
        while True:
            if dongle_check(self):
                break
            time.sleep(1)
    self.logger.info(f"ADC　USBドングル　認識")

def dongle_check_process(self):
    dev = usb.core.find(
        idVendor=self.dic["USBドングル"]["VENDOR_ID"],
        idProduct=self.dic["USBドングル"]["PRODUCT_ID"]
        )
    if dev is not None:
        # 該当のUSBドングルが挿さっています。
        return True
    else:
        # ドングルが見つかりません。
        return False
