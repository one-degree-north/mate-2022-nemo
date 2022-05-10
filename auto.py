from controls import Controls
#includes gyro tilt automation, (maybe) stopping thrust when not holding down, water already does this though
class Automation:
    def __init__(self, controls):
        self.controls = controls
    def statGyroAutomationLoopThread(self): #automatically corrects bot tilt position
        
        pass
    def stopGyroAutomationLoopThread(self): #stops correcting tilt position
        
        pass
    def gyroAutomationLoop(self):
        if (self.controls.gyroData[0] > 10):
            pass
        elif (self.controls.gyroData[0] < -10):
            pass

class TiltCompensation:
    def __init__(self, controls):
        self.targetTilt = 0
        self.currTilt = 90
        self.tiltSpeed = 3
        self.tiltMotorArr = [-50, 50]
    def startThread(self):
        pass
    def compensateTilt(self):
        deltaTilt = self.currTilt / 180
        print(deltaTilt)
        deltaTiltArr = []
        for motorStrength in self.tiltMotorArr:
            deltaTiltArr.append(motorStrength * deltaTilt)
            print(motorStrength * deltaTilt)
        return deltaTiltArr
        #move thrusters by tiltSpeed * deltaTilt. If negative, move 

if (__name__ == "__main__"):
    print("AAA")
    tilt = TiltCompensation(None)
    tilt.currTilt
    tilt.compensateTilt()