import serial

def clean_text(data: bytes) -> str:
    """
    受信したバイト列をデコードし、
    改行・スペース・% を取り除いて返す。
    """
    text = data.decode('utf-8', errors='ignore')
    # 先頭・末尾の改行や空白は strip() で除去
    text = text.strip()
    # 文章中のスペースや % をさらに除去
    text = text.replace(' ', '').replace('%', '')
    return text

def serial_setup():
    try:
        ser = serial.Serial(
            port="COM10",
            baudrate=19200,
            bytesize=8,
            parity='E',
            stopbits=2,
            rtscts=True
        )
        while True:
            row = ser.readline()
            txt = clean_text(row)
            print(txt)
    except Exception as e:
        # 切断状態
        print("An error occurred:", e)

if __name__ == "__main__":
    serial_setup()