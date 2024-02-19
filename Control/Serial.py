import serial
import serial.tools.list_ports
from threading import Thread

rbSer = None
connectd = True

def serial_listen(ser):
    while True:
        line = ser.readline()
        if line.decode() != "" and line.decode() != "\n":
            pline = line.decode().replace("\n", "")
            print(pline)

def serial_send(ser, message):
    ser.write(message.encode())

#COM PORT STUFF
ports = list(serial.tools.list_ports.comports())
for p in ports:
    rbSer = serial.Serial(p[0], 9600, timeout=10)
    line = rbSer.readline()
    print(line.decode())
    serial_send(rbSer, "<sp2414>\n")
    line = rbSer.readline()
    if "<sp2414>" in line.decode():
        print(line.decode())
        connectd = True
    if connectd == True:
        break

#MAIN BODY OF OPERATION
#TODO: Move this thread to main control body code when it is created.
#TODO: Ideally, we'll be able to use the functions in this file for something like a cpp-style include 

thread = Thread(target=serial_listen, args=(rbSer))
thread.start()

while connectd == True:
    pass