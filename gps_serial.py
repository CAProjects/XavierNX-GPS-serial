import serial
from time import sleep

port = "/dev/ttyTHS0"
ser = serial.Serial(port, baudrate=9600)
while True:
    sleep(1)
    ser.write(b'A')
    nbChars = ser.inWaiting()
    if nbChars>0:
        data = ser.read(nbChars)
        print(data)
