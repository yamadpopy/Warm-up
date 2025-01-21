import serial
import time
import random

com_txt_list = [
    "STARTWWG01WWX1.0WWY3.0WWZ50.5WW5.015",
    "DATAWWG01WWX100.0WWY150.0WWZ50.5WW7.456",
    "DATAWWG03WWX150.0WWY250.0WWZ50.5WW9.456",
    "ENDWWG02WWX250.0WWY350.0WWZ150.5WW13.87",
]

serial_para = serial.Serial(
            port="COM4",
            baudrate=19200,
            bytesize=8,
            parity=serial.PARITY_EVEN,
            stopbits=2
            )

for com_txt in com_txt_list:
    time.sleep(random.uniform(3,9))
    serial_para.write((com_txt+"\r\n").encode())
    print(com_txt)

