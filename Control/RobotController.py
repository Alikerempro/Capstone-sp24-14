from multiprocessing.connection import Listener
from threading import Thread
import json
import serial
import serial.tools.list_ports
import time

####
## ROBOT CONTROL FUNCTIONS
####

def turnRobot(direction, ser): #direction [-1:1], values <0 are counterclockwise, values >0 are clockwise
    serial_send(ser, {
                "id": "sp2414",
                "type" : "turn",
                "dir" : direction,
                "dur" : 0.2
            })
        
    time.sleep(0.2)
    return

def moveRobot(direction, ser): #direction [-1:1], values <0 are reverse, values >0 are forward
    serial_send(ser, {
                "id": "sp2414",
                "type" : "move",
                "dir" : direction
            })
    return

def engageSampler(io, ser): #io = True means sampler will be engaged. False means it will be disengaged.
    serial_send(ser, {
                "id": "sp2414",
                "type" : "sampler",
                "dir" : io
            })
    return

def serial_send(ser, message): #
    ser.write(("<" + json.dumps(message) + ">").encode())
    print("Sending... " + "<" + json.dumps(message) + ">")

####
## GLOBAL VARS AND SETUP
####

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'sp2414')
conn = listener.accept()
rbSer = None
connectd = False

ports = list(serial.tools.list_ports.comports())
print(ports)
for p in ports:
    print("looping ")
    rbSer = serial.Serial(p[0], 9600, timeout=5)
    line = rbSer.readline()
    print(line)
    serial_send(rbSer, {
        "id": "sp2414", 
        "type": "connect"})
    line = rbSer.readline()
    try:
        if "good" in json.loads(line.decode()):
            print(line.decode())
            connectd = True
            print("Connected!")
    except:
        continue
    if connectd == True:
        break

####
## ASYNC FUNCTIONS
####

def listenSerial(ser):
    enabled = True
    while enabled:
        line = ser.readline()
        if line.decode() != "" and line.decode() != "\n":
            pline = line.decode().replace("\n", "")
            print("Received... " + pline)
    return

def listenIPC(ser):
    enabled = True
    while enabled:
        command = json.loads(conn.recv())
        
        ## Computer vision parsing
        if command["source"] == "CV":
            ## If robot controller hears about an obstacle, it turns the robot to avoid it
            if "obstacle" in command:
                if command["obstacle"] == "l":
                    turnRobot(-1, ser)
                elif command["obstacle"] == "r":
                    turnRobot(1, ser)
                    
        ## Manual control parsing
        elif command["source"] == "manual":
            if "turn" in command:
                turnRobot(command["turn"], ser)
            if "move" in command:
                moveRobot(command["move"], ser)
            if "sampler" in command:
                engageSampler(command["sampler"], ser)
                
        ## Special commands
        if "exit" in command:
            serial_send(ser, {
                "id": "sp2414",
                "type" : "exit"
            })
            conn.close
            enabled = False
            break
        
    return

####
## MAIN OPERATION
####

thread1 = Thread(target=listenSerial, args=(rbSer,))
thread1.start()

thread2 = Thread(target=listenIPC, args=(rbSer,))
thread2.start()


listener.close()