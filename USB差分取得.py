import wmi
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

def get_connected_devices():
    """
    現在接続されているPnPエンティティ(デバイス)の一覧を返す
    (DeviceID をキーとしてセットで返す)
    """
    w = wmi.WMI()
    devices = w.Win32_PnPEntity()  # 全てのPnPデバイスを取得
    # DeviceID は '\\\\?\\USB#VID_XXXX&PID_XXXX#...' などの文字列
    # または他のバスの場合は別のフォーマットの場合あり
    device_ids = {device.DeviceID for device in devices}
    return device_ids

def get_usb_devices():
    """
    USB接続デバイスらしきものをざっくり取得し、(DeviceID, Name) のペアを返す
    """
    w = wmi.WMI()
    devices = w.Win32_PnPEntity()
    usb_list = []
    for device in devices:
        # "USB" が含まれている場合、USBデバイス(もしくはUSB経由)と思われる
        # 必ずしも完璧ではないので必要に応じてフィルタを詳細化する
        if "USB" in (device.Name or "") or "USB" in (device.DeviceID or ""):
            usb_list.append((device.DeviceID, device.Name))
    return usb_list

def detect_new_devices(before_set, after_set):
    """
    before_set, after_set: デバイスの DeviceID のセット
    新規に追加されたデバイスのセットを返す
    """
    return after_set - before_set  # 差分(後から見て増えたもの)

def main():
    print("1) USB挿す前のデバイスを取得します...")
    before_devices = get_connected_devices()

    input("2) USBドングルを挿したらEnterを押してください...")

    print("3) USB挿した後のデバイスを取得します...")
    after_devices = get_connected_devices()

    # 差分を取る
    new_device_ids = detect_new_devices(before_devices, after_devices)

    if not new_device_ids:
        print("新しく追加されたデバイスは見つかりませんでした。")
        return

    print("新しく追加されたデバイスのDeviceIDは以下の通り:")
    for dev_id in new_device_ids:
        print("  ", dev_id)

    print("\nUSBデバイス情報(全体)を取得します...")
    usb_list = get_usb_devices()
    # 新しく追加されたデバイスの中に該当するものがあるかを探す
    new_usb_devices = [dev for dev in usb_list if dev[0] in new_device_ids]

    if new_usb_devices:
        print("新たに追加されたUSBデバイスと思われる情報:")
        for dev_id, dev_name in new_usb_devices:
            print(f"  DeviceID: {dev_id}")
            print(f"  Name    : {dev_name}")
            print()
    else:
        print("新たに追加されたデバイスの中にUSBデバイスは見つかりませんでした。")

if __name__ == "__main__":
    main()