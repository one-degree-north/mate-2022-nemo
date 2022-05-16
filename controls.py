from comms import Comms
import queue
#import asyncio
# a change
import time

class Controls:
    def __init__(self):
        #self.comms = Comms()
        self.gyroData = [0, 0, 0]
        self.accelData = [0, 0, 0]

        self.tempData = 0
        self.clawOpen = False
        self.clawOpenDeg = 10
        self.clawClosedDeg = 80
        self.outputQueue = queue.Queue()
        self.comms = Comms(outputQueue=self.outputQueue, controls=self)

        #should I implement claw rotating this way?
        self.rotateRotateServo = False
        self.rotateClockwise = True
        self.loopStartTime = time.time()
        self.rotateSpeed = 5
        self.currRotateDeg = 0
        self.deltaTime = 0
        
        self.cameraServo = 0
        self.clawRotateServo = 1
        self.clawServo = 2
        
        self.frontLThruster = 1
        self.frontRThruster = 0
        self.midLThruster = 2
        self.midRThruster = 5
        self.backLThruster = 4
        self.backRThruster = 3
        self.cameraServo = 2
        self.clawRotateServo = 0
        self.clawServo = 1
        self.topSpeed = 200
        self.minSpeed = 100
        self.currClawDeg = 0 # just the claw's clamp thingy
        self.currClawRotateDeg = 0 # whole claw thingy
        self.currCameraServoDeg = 0
        self.rotateRight = False
        self.rotateLeft = False

        self.flip = [
            self.midLThruster,
            self.frontLThruster, 
            self.frontRThruster,
        ]

        self.reversed = [
            self.frontLThruster,
            self.frontRThruster,
            self.backLThruster,
            self.backRThruster
        ]


    def startThread(self):
        self.comms.startThread()
        print("start thread")

    def thrusterOn(self, motor, speed):
        #Testing, having the input between -50 and 50 instead
        """if motor not in self.flip:
            speed *= -1 # MAJOR SPEED FLIP THING
        if motor in self.reversed:
            speed *= -1
            
        speed += 150"""
        #TESTING higher microseconds
        #speed *= 1.15

        # flip = [0, 1, 4]
        flip = [3]
        if motor in flip:
            speed = -speed



        speed = speed + 150
        speed = int(speed)

        if speed > 200:
            speed = 200
        elif speed < 100:
            speed = 100



        self.outputQueue.put((0x20, [motor, speed]))
        #self.comms.write(0x20, [motor, speed])

    def thrusterOff(self, motor):
        self.outputQueue.put((0x20, [motor, 150]))
        #self.comms.write(0x20, [motor, 0])

    def getGyroData(self):
        self.outputQueue.put((0x30, [0x12]))
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
            print("AAAAAA")
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
        print(returnBytes)
        #returnBytes = self.comms.read()
        if (returnBytes == -1):
            #print("rip")
            return -1
        
        command = returnBytes[0]
        #print(chr(command))
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
        print("updating accel")
        if (returnBytes[1] == bytes.fromhex("00")):
            self.accelData[0] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("30")):
            self.accelData[1] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("60")):
            self.accelData[2] = returnBytes[2]

    def handleGyroReturn(self, returnBytes):
        print("updating gyro")
        print(returnBytes[2])
        if (returnBytes[1] == bytes.fromhex("00")):
            self.gyroData[0] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("30")):
            self.gyroData[1] = returnBytes[2]
        elif(returnBytes[1] == bytes.fromhex("60")):
            self.gyroData[2] = returnBytes[2]

    def loop(self):
        loopStartTime = time.time()
        self.deltaTime = loopStartTime-self.startTime
        if (self.rotateRotateServo):
            self.rotateContinuously()
        self.startTime = loopStartTime

    def rotateContinuously(self):
        #doesn't warrent creating an entirely new class for commands yet
        if (self.rotateClockwise):
            self.currRotateDeg += self.rotateSpeed * self.deltaTime
        else:
            self.currRotateDeg -= self.rotateSpeed * self.deltaTime
        if (self.currRotateDeg < 0):
            self.currRotateDeg = 0
        if (self.currRotateDeg > 180):
            self.currRotateDeg = 180
        self.setClawDeg(self.clawRotateServo, self.currRotateDeg)

    def moveFront(self, strength):
        thrusterStrength = strength
        reverseThrusterStrength = strength * -1
        self.thrusterOn(self.frontRThruster, int(reverseThrusterStrength))
        self.thrusterOn(self.frontLThruster, int(reverseThrusterStrength))
        self.thrusterOn(self.backRThruster, int(reverseThrusterStrength))
        self.thrusterOn(self.backLThruster, int(reverseThrusterStrength))

    def moveSide(self, strength):
        thrusterStrength = strength
        reverseThrusterStrength = strength * -1
        self.thrusterOn(self.frontRThruster, int(thrusterStrength))
        self.thrusterOn(self.frontLThruster, int(thrusterStrength))
        self.thrusterOn(self.backRThruster, int(thrusterStrength))
        self.thrusterOn(self.backLThruster, int(thrusterStrength))

    def rotate(self, strength):
        thrusterStrength = strength
        reverseThrusterStrength = strength * -1
        self.thrusterOn(self.frontRThruster, int(thrusterStrength))
        self.thrusterOn(self.backRThruster, int(thrusterStrength))
        self.thrusterOn(self.backLThruster, int(reverseThrusterStrength))
        self.thrusterOn(self.frontLThruster, int(reverseThrusterStrength))
        pass

    def moveUp(self, strength):
        thrusterStrength = strength
        reverseThrusterStrength = strength * -1
        self.thrusterOn(self.midLThruster, int(thrusterStrength))  
        self.thrusterOn(self.midRThruster, int(thrusterStrength))

    def tilt(self, strength, direction): #true is right, false is left
        thrusterStrength = strength
        reverseThrusterStrength = strength * -1
        if (direction):
            self.thrusterOn(self.midLThruster, int(thrusterStrength))
        else:
            self.thrusterOn(self.midRThruster, int(thrusterStrength))

    def halt(self):
        self.thrusterOn(self.frontRThruster, 0)
        self.thrusterOn(self.frontLThruster, 0)
        self.thrusterOn(self.backRThruster, 0)
        self.thrusterOn(self.backLThruster, 0)
        self.thrusterOn(self.midRThruster, 0)
        self.thrusterOn(self.midLThruster, 0)

    def moveClaw(self, deg):
        if (deg > 90):
            deg = 90
        if (deg < 0):
            deg = 0
        self.setClawDeg(self.clawServo, deg)

    def moveRotateServo(self, incrementDeg):
        self.currClawRotateDeg += incrementDeg
        if (self.currClawRotateDeg < 0):
            self.currClawRotateDeg = 0
        if (self.currClawRotateDeg > 180):
            self.currClawRotateDeg = 180
        self.setClawDeg(self.clawRotateServo, self.currClawRotateDeg)

    def moveCameraServo(self, incrementDeg):
        self.currCameraServoDeg += incrementDeg
        if (self.currCameraServoDeg < 0):
            self.currCameraServoDeg = 0
        if (self.currCameraServoDeg > 180):
            self.currCameraServoDeg = 180
        self.setClawDeg(self.cameraServo, self.currCameraServoDeg)

    @staticmethod
    def getThrusterStrength(input): #turns an input of -50 to 50 into a value between 100 and 200
        return input + 150
    @staticmethod
    def invertStrength(input): #turns an input of -50 to 50 into an inverted value between 100 and 200
        return -1*input+150


    """def testCommControlQueue(self):

        while True:
            if (self.arduinoSerial.in_waiting >= 7):
                self.handleInput(self.read())
            if (self.outputQueue.not_empty):
                self.comms.write(self.inputQueue.get())
            if (self.inputQueue.not_empty):"""
