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
        targetTilt = 90
        currTilt = 90
        tiltSpeed = 3
        tiltMotorArr = [50, -50, -50, 50]
        pass
    def startThread(self):
        pass
    def copensateTilt(self):
        #update currentTilt
        deltaTilt = (self.currTilt - self.targetTilt) % 360
        if (deltaTilt < 0):
            deltaTilt + 360
        if (abs(deltaTilt) > 180):
            deltaTilt -= 180
            deltaTilt  *= -1
        deltaTiltArr = []
        for motorStrength in self.tiltMotorArr:
            deltaTiltArr.append(motorStrength * deltaTilt)
        
        #move thrusters by tiltSpeed * deltaTilt. If negative, move 
    pass