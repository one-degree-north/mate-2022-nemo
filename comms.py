import threading, queue, time, struct
from serial import *


class Comms:
    def __init__(self, outputQueue=None, controls=None):
        self.arduinoSerial = Serial(port="/dev/cu.usbmodem14101" ,baudrate=9600)
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
        #print("reading")
        #print("READING STUFF")
        currLength = 1
        currByte = self.arduinoSerial.read()
        footerFound = False
        printResults = True
        headerFound = False
        print("currByte")
        print(currByte)
        while (not headerFound):
            if (currByte == self.HEADER):
                headerFound = True
                returnValue = self.arduinoSerial.read_until(expected=self.FOOTER, size=7)
                if (returnValue[-1] == self.INTFOOTER):
                    footerFound=True
                    break
                #print(testResult)
                """
                while (currLength <= 5):
                    currByte = self.arduinoSerial.read()
                    currLength += 1
                    if (currByte == self.FOOTER):
                        footerFound = True
                        break
                    returnValue.append(currByte)
                    currLength += 1
                """
            currByte = self.arduinoSerial.read()
            print("currByte")
            print(currByte)
            #else:
                #not too sure if I should do this
            #    self.read()
            #    print("hmmmm")
        print(returnValue)
        if (len(returnValue) != 7):
            print("not enough bytes to eat")
            print(returnValue)
            return -1
        structValue = struct.unpack("=ccfc", returnValue)
        #print(structValue)
        #print(struct.unpack("bbbb", returnValue))
        #print(struct.unpack("cccc", returnValue))
        if (headerFound):
            #if (printResults):
            #    print("---")
            #    print("return array: ")
            #    print(returnValue)
            #    print("footer found: " + str(footerFound))

            if (footerFound):
                #print("returning stuff yey!")
                return structValue
            else:
                return -1
        else:
            print("header not fooking found")
            pass

    def write(self, command, params):
        print("writing")
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
            #print("wtf??")
            if (self.arduinoSerial.in_waiting >= 7):
                print("INPUT WOAH")
                self.controls.handleInput(self.read())
            if (not self.outputQueue.empty()):
                print("output queue not empty")
                currOutputValue = self.outputQueue.get()
                print("got currQueue")
                print(currOutputValue[0])
                print(currOutputValue[1])
                self.write(currOutputValue[0], currOutputValue[1])
            
            #if (self.arduinoSerial.in_waiting > 0):
            #    print("input???")
            #if (self.arduinoSerial.out_waiting > 0):
            #    print("output???")

    def startThread(self):
        print("B")
        currThread = threading.Thread(target=self.commThread)
        currThread.start()
        print("B")
        #return currThread

