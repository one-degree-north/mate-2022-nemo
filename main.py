from Comms import Comms
import time, queue

class Controls:
    def __init__(self):
        self.comms = Comms()
        self.gyroData = [0, 0, 0]
        self.accelData = [0, 0, 0]

        self.tempData = 0
        self.clawOpen = False
        self.clawOpenDeg = 10
        self.clawClosedDeg = 80
        self.outputQueue = queue.Queue()
        self.comms = Comms(outputQueue=self.outputQueue, controls=self)

    def startThread(self):
        self.comms.startThread()
        print("start thread")

    def thrusterOn(self, motor, speed):
        self.outputQueue.put([(0x20), [motor, speed]])
        #self.comms.write(0x20, [motor, speed])

    def thrusterOff(self, motor):
        self.outputQueue.put([0x20, [motor, 150]])
        #self.comms.write(0x20, [motor, 0])

    def getGyroData(self):
        self.outputQueue.put([0x30, [0x12]])
        #self.comms.write(0x30, 0x12)
    
    def setClawDeg(self, selectedServo=0, servoDeg=None):
        if (servoDeg == None):
            if (self.clawOpen):
                #print(self.clawClosedDeg)
                self.outputQueue.put([0x23, [selectedServo, self.clawClosedDeg]])
                #self.comms.write(0x23, [selectedServo, self.clawClosedDeg])
            else:
                #print(self.clawOpenDeg)
                #print([0x23, [selectedServo, self.clawOpenDeg]])
                self.outputQueue.put([0x23, [selectedServo, self.clawOpenDeg]])
                #self.comms.write(0x23, [selectedServo, self.clawOpenDeg])
            self.clawOpen = not self.clawOpen
        else:
            self.outputQueue.put((0x23, [selectedServo, servoDeg]))
            #self.comms.write(0x23, [selectedServo, servoDeg])

    def getAccelData(self):
        #self.comms.write(0x30, [0x10])
        self.outputQueue.put((0x30, [0x10]))

    def setAutoReport(self, command=None, milliseconds=100):
        commands = [0x1C, 0x1D, 0x1E, 0x1F]
        print(command)
        if (not command in commands):
            return -1
        else:
            self.outputQueue.put((0x50, [command, milliseconds]))
            #self.comms.write(0x50, [command, milliseconds])
        if command==None:
            for command in commands:
                self.outputQueue.put((0x50, [command, milliseconds]))
                #self.comms.write(0x50, [command, milliseconds])

    def handleInput(self, returnBytes):
        #what the hell
        #print("handling input:")
        #returnBytes = self.comms.read()
        if (returnBytes == -1):
            #print("rip")
            return -1
        
        command = returnBytes[0]
        #print(command)
        #print(type(command))
        value = returnBytes[1]
        if (command == bytes.fromhex("1C")):
            self.handleAccelReturn(returnBytes)
        elif (command == bytes.fromhex("1D")):
            self.tempData = returnBytes[0]
        elif (command== bytes.fromhex("1E")):
            self.handleGyroReturn(returnBytes)
        elif(command == bytes.fromhex("1F")):
            pass

    def handleInputQueue(self):
        pass

    def handleAccelReturn(self, returnBytes):
        #print("updating accel")
        if (returnBytes[1] == bytes.fromhex("00")):
            self.accelData[0] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("30")):
            self.accelData[1] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("60")):
            self.accelData[2] = returnBytes[2]

    def handleGyroReturn(self, returnBytes):
        #print("updating gyro")
        if (returnBytes[1] == bytes.fromhex("00")):
            self.gyroData[0] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("30")):
            self.gyroData[1] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("60")):
            self.gyroData[2] = returnBytes[2]

    """def testCommControlQueue(self):

        while True:
            if (self.arduinoSerial.in_waiting >= 7):
                self.handleInput(self.read())
            if (self.outputQueue.not_empty):
                self.comms.write(self.inputQueue.get())
            if (self.inputQueue.not_empty):"""


def main():
    comms = Comms()
    controls = Controls(comms)
    controls.setAutoReport(command=0x1C)
    controls.setAutoReport(command=0x1E)

def testServo():
    comms = Comms()
    controls = Controls(comms)
    controls.getAccelData()
    while True:
        if (input()):
            controls.setClawDeg(selectedServo=0)
            comms.readOneByte()
    pass   
    
def testAutoReport():
    comms = Comms()
    controls = Controls(comms)
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
        pass
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

if(__name__ == "__main__"):
    #test()
    #main()
    #testServo()
    #testCommThreading2()
    testThruster()
