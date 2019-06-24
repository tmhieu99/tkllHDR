import serial
ser = serial.Serial("COM3", 115200, timeout=1)
a = b'0'
for i in range(783):
    a = a + bytes(',' + str((i + 1) % 256), 'utf-8')
a = a + b'\n'
