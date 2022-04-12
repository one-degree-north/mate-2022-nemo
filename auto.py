from controls import Controls
#includes gyro tilt automation, (maybe) stopping thrust when not holding down, water already does this though
class Automation:
    def __init__(self, controls):
        self.controls = controls
    def statGyroAutomationLoopThread(self): #automatically corrects bot tilt position 
        pass
    def stopGyroAutomationLoopThread(self):
        pass
    def gyroAutomationLoop(self):
        if (self.controls.gyroData[0] > 10):
            pass
        elif (self.controls.gyroData[0] < -10):
            pass