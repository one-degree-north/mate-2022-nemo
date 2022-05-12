import threading, queue, time, struct
from serial import *


class Comms:
    def __init__(self, outputQueue=None, controls=None):
        port_no = int(input("port no: "))
        #self.arduinoSerial = Serial(port=f"/dev/ttyUSB{port_no}", baudrate=9600)
        self.arduinoSerial = Serial(port=f"/dev/ttyS0", baudrate=9600)
        # "/dev/ttyS0"
        #"/dev/cu.usbmodem14201"
        #eh make these static
        self.HEADER = bytes.fromhex("AB")
        self.FOOTER = bytes.fromhex("B3")
        self.INTFOOTER = 179
        self.outputQueue = outputQueue
        self.controls = controls

    def readOneByte(self):
        test = self.arduinoSerial.read()
        print(test)


    def read(self):
        currByte = self.arduinoSerial.read()
        footerFound = False
        headerFound = False
        #print("currByte")
        #print(currByte)
        while (not headerFound):
            if (currByte == self.HEADER):
                headerFound = True
                returnValue = self.arduinoSerial.read_until(expected=self.FOOTER, size=7)
                if (returnValue[-1] == self.INTFOOTER):
                    footerFound=True
                    break
            currByte = self.arduinoSerial.read()
        #print(returnValue)
        if (len(returnValue) != 7):
            return -1
        structValue = struct.unpack("=ccfc", returnValue)
        if (headerFound):
            if (footerFound):
                return structValue
            else:
                return -1

    def write(self, command, params):
        #print("writing")
        #print(command)
        #print(params)
        self.arduinoSerial.write(self.HEADER)
        self.arduinoSerial.write(command.to_bytes(1, byteorder="big"))
        for i in range(len(params)):
            self.arduinoSerial.write(params[i].to_bytes(1, byteorder="big"))
        self.arduinoSerial.write(self.FOOTER)

    def setBaudRate(self, baudrate):
        self.arduinoSerial.baudrate = baudrate

    def setPort(self, port):
        self.arduinoSerial.port = port

    def getInfoDict(self):
        pass

    def commThread(self):
        while True:
            if (self.arduinoSerial.in_waiting >= 7):
                #print("reading sensor input")
                self.controls.handleInput(self.read())
            if (not self.outputQueue.empty()):
                currOutputValue = self.outputQueue.get()
                self.write(currOutputValue[0], currOutputValue[1])

    def startThread(self):
        #print("B")
        currThread = threading.Thread(target=self.commThread)
        currThread.start()
        print("B")
        #return currThread

