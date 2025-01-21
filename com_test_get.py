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

def main():
    # シリアルポートを開く
    with serial.Serial(
        port="COM10",
        baudrate=19200,
        bytesize=8,
        parity='E',
        stopbits=2,
        rtscts=True
    ) as ser:
        print("Serial port is open with RTS/CTS enabled.")
        while True:
            row = ser.readline()
            txt = clean_text(row)
            print(txt)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting.")
    except Exception as e:
        print("An error occurred:", e)