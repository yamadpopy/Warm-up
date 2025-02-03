# -*- coding: utf-8 -*-
import usb.core
import usb.util

VENDOR_ID = 0x096E  # 0x096E
PRODUCT_ID = 0x0006 # 0x0006

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is not None:
    print("該当のUSBドングルが挿さっています。")
else:
    print("ドングルが見つかりません。")
