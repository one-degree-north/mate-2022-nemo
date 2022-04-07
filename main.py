from comms import Comms
from controls import Controls
import time, queue

def main():
    controls = Controls()
    controls.setAutoReport(command=0x1C)
    controls.setAutoReport(command=0x1E)

def testServo():
    controls = Controls()
    #controls.getAccelData()
    while True:
        if (input()):
            controls.setClawDeg(selectedServo=0)
            #comms.readOneByte()
    pass   
    
def testAutoReport():
    controls = Controls()
    controls.setAutoReport(command=0x1C)
    controls.setAutoReport(command=0x1E)
    
    while True:
        controls.handleInput()
        controls.handleInput()
        controls.handleInput()
        controls.handleInput()
        controls.handleInput()
        controls.handleInput()
        print("gyro data: ")
        print(controls.gyroData)
        print("accelData: ")
        print(controls.accelData)
        time.sleep(1)

def test():
    comms = Comms()
    controls = Controls(comms)
    controls.getAccelData()
    comms.read()
    comms.read()
    comms.read()

def testCommThreading():
    controls= Controls()
    controls.startThread()
    controls.setAutoReport(command=0x1C)
    controls.setAutoReport(command=0x1E)
    while True:
        print(controls.gyroData)
        print(controls.accelData)
        pass
        #print(controls.gyroData)
        #if (input()):
        #    controls.setClawDeg(selectedServo=0)
def testCommThreading2():
    controls=Controls()
    controls.startThread()
    controls.getAccelData()
    while True:
        if (input()):
            controls.setClawDeg(selectedServo=0)

def testThruster():
    controls=Controls()
    controls.startThread()
    while True:
        currMotor = int(input())
        currSpeed = int(input())
        controls.thrusterOn(currMotor, currSpeed)
#def testCommThreading2():
#    pass
def testServo2():
    controls=Controls()
    controls.startThread()
    while True:
        currServo = int(input())
        currDeg = int(input())
        #print(currServo)
        #print(currDeg)
        controls.setClawDeg(selectedServo=currServo, servoDeg=currDeg)
    pass

if(__name__ == "__main__"):
    #test()
    #main()
    #testServo()
    #testCommThreading()
    #testThruster()
    testServo2()