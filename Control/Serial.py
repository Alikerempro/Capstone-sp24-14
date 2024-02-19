import serial
import serial.tools.list_ports
from threading import Thread
import socket
import time
import os

def listen(ser):
    while True:
        line = ser.readline()
        if line.decode() != "" and line.decode() != "\n":
            pline = line.decode().replace("\n", "")
            print(pline)

rbSer = None
connectd = True

#COM PORT STUFF
ports = list(serial.tools.list_ports.comports())
for p in ports:
    rbSer = serial.Serial(p[0], 9600, timeout=10)
    line = rbSer.readline()
    print(line.decode())
    rbSer.write("<sp2414>\n".encode())
    line = rbSer.readline()
    if "<sp2414>" in line.decode():
        print(line.decode())
        connectd = True
    if connectd == True:
        break

#MAIN BODY OF OPERATION

thread = Thread(target=listen, args=(rbSer))
thread.start()

while connectd == True:
    pass