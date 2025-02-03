# -*- coding: utf-8 -*-
import usb.core
import usb.util

def dongle_check(self):
    dev = usb.core.find(
        idVendor=self.dic["USBドングル"]["VENDOR_ID"],
        idProduct=self.dic["USBドングル"]["PRODUCT_ID"]
        )
    if dev is not None:
        print("該当のUSBドングルが挿さっています。")
        return True
    else:
        print("ドングルが見つかりません。")
        return False
