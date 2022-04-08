"""
Uses xboxdrv and pygame
Works on Linux only

Before running this script, xboxdrv should be running

Buttons that are either pressed or not pressed (value = 0 or 1)
A -> 6
B -> 7
X -> 8
Y -> 9

Right B -> 11
Left B -> 10

Cross-shaped button -> 17 [up/down: (0, ±1), right/left: (±1, 0)]


Buttons that have many values (each usually ranges from 0 to 100)
Right trigger -> 5 [100 when pressed, 0 when not pressed]
Left trigger -> 2 [100 when pressed, -100 when not pressed]

Left DPAD
    Horizontal means X-axis -> 0 Ranges from -100(left) to 100 (right)
    Vertical means Y-axis -> 1 Ranges from -100(down) to 100 (up)
"""



import pygame
from pygame.locals import *
from pygame.time import Clock
import os, sys
import threading
import time
from controls import Controls
# Start xboxdrv
# os.system("sudo jstest /dev/input/js0")
# Probably shouldn't run this thingy

pygame.time
"""
NOTES - pygame events and values

JOYAXISMOTION
event.axis              event.value
0 - x axis left thumb   (+1 is right, -1 is left)
1 - y axis left thumb   (+1 is down, -1 is up)
2 - x axis right thumb  (+1 is right, -1 is left)
3 - y axis right thumb  (+1 is down, -1 is up)
4 - right trigger
5 - left trigger

JOYBUTTONDOWN | JOYBUTTONUP
event.button
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
XBOX = 8
LEFTTHUMB = 9
RIGHTTHUMB = 10

JOYHATMOTION
event.value
[0] - horizontal
[1] - vertival
[0].0 - middle
[0].-1 - left
[0].+1 - right
[1].0 - middle
[1].-1 - bottom
[1].+1 - top

"""

# Main class for reading the xbox controller values
class XboxController(threading.Thread):


    # Internal ids for the xbox controls
    class XboxControls():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5
        A = 6
        B = 7
        X = 8
        Y = 9
        LB = 10
        RB = 11
        BACK = 12
        START = 13
        XBOX = 14
        LEFTTHUMB = 15
        RIGHTTHUMB = 16
        DPAD = 17

    # Pygame axis constants for the analogue controls of the xbox controller
    class PyGameAxis():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5

    # Pygame constants for the buttons of the xbox controller
    class PyGameButtons():
        A = 0
        B = 1
        X = 2
        Y = 3
        LB = 4
        RB = 5
        BACK = 6
        START = 7
        XBOX = 8
        LEFTTHUMB = 9
        RIGHTTHUMB = 10

    # Map between pygame axis (analogue stick) ids and xbox control ids
    AXISCONTROLMAP = {PyGameAxis.LTHUMBX: XboxControls.LTHUMBX,
                      PyGameAxis.LTHUMBY: XboxControls.LTHUMBY,
                      PyGameAxis.RTHUMBX: XboxControls.RTHUMBX,
                      PyGameAxis.RTHUMBY: XboxControls.RTHUMBY}
    
    # Map between pygame axis (trigger) ids and xbox control ids
    TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: XboxControls.RTRIGGER,
                         PyGameAxis.LTRIGGER: XboxControls.LTRIGGER}

    # Map between pygame buttons ids and xbox contorl ids
    BUTTONCONTROLMAP = {PyGameButtons.A: XboxControls.A,
                        PyGameButtons.B: XboxControls.B,
                        PyGameButtons.X: XboxControls.X,
                        PyGameButtons.Y: XboxControls.Y,
                        PyGameButtons.LB: XboxControls.LB,
                        PyGameButtons.RB: XboxControls.RB,
                        PyGameButtons.BACK: XboxControls.BACK,
                        PyGameButtons.START: XboxControls.START,
                        PyGameButtons.XBOX: XboxControls.XBOX,
                        PyGameButtons.LEFTTHUMB: XboxControls.LEFTTHUMB,
                        PyGameButtons.RIGHTTHUMB: XboxControls.RIGHTTHUMB}
                        
    # Setup xbox controller class
    def __init__(self,
                 controllerCallBack = None,
                 joystickNo = 0,
                 deadzone = 0.1,
                 scale = 1,
                 invertYAxis = False):

        #setup threading
        threading.Thread.__init__(self)
        
        # Persist values
        self.running = False
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.lowerDeadzone = deadzone * -1
        self.upperDeadzone = deadzone
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        # Setup controller properties
        self.controlValues = {self.XboxControls.LTHUMBX:0,
                              self.XboxControls.LTHUMBY:0,
                              self.XboxControls.RTHUMBX:0,
                              self.XboxControls.RTHUMBY:0,
                              self.XboxControls.RTRIGGER:0,
                              self.XboxControls.LTRIGGER:0,
                              self.XboxControls.A:0,
                              self.XboxControls.B:0,
                              self.XboxControls.X:0,
                              self.XboxControls.Y:0,
                              self.XboxControls.LB:0,
                              self.XboxControls.RB:0,
                              self.XboxControls.BACK:0,
                              self.XboxControls.START:0,
                              self.XboxControls.XBOX:0,
                              self.XboxControls.LEFTTHUMB:0,
                              self.XboxControls.RIGHTTHUMB:0,
                              self.XboxControls.DPAD:(0,0)}

        # Setup pygame
        self._setupPygame(joystickNo)

    # Create controller properties
    @property
    def LTHUMBX(self):
        return self.controlValues[self.XboxControls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self.controlValues[self.XboxControls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self.controlValues[self.XboxControls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self.controlValues[self.XboxControls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self.controlValues[self.XboxControls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self.controlValues[self.XboxControls.LTRIGGER]

    @property
    def A(self):
        return self.controlValues[self.XboxControls.A]

    @property
    def B(self):
        return self.controlValues[self.XboxControls.B]

    @property
    def X(self):
        return self.controlValues[self.XboxControls.X]

    @property
    def Y(self):
        return self.controlValues[self.XboxControls.Y]

    @property
    def LB(self):
        return self.controlValues[self.XboxControls.LB]

    @property
    def RB(self):
        return self.controlValues[self.XboxControls.RB]

    @property
    def BACK(self):
        return self.controlValues[self.XboxControls.BACK]

    @property
    def START(self):
        return self.controlValues[self.XboxControls.START]

    @property
    def XBOX(self):
        return self.controlValues[self.XboxControls.XBOX]

    @property
    def LEFTTHUMB(self):
        return self.controlValues[self.XboxControls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self.controlValues[self.XboxControls.RIGHTTHUMB]

    @property
    def DPAD(self):
        return self.controlValues[self.XboxControls.DPAD]

    # Setup pygame
    def _setupPygame(self, joystickNo):
        # Set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # Init pygame
        pygame.init()
        # Create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # Init the joystick control
        pygame.joystick.init()
        # How many joysticks are there
        # Print pygame.joystick.get_count()
        # Get the first joystick
        joy = pygame.joystick.Joystick(joystickNo)
        # Init that joystick
        joy.init()

    # Called by the thread
    # I think this extends the run() method of Thread ~ Kevin
    def run(self):
        self._start()

    # Start the controller
    def _start(self):
        
        self.running = True
        
        # Run until the controller is stopped
        while(self.running):
            # React to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                # Thumb sticks, trigger buttons                    
                if event.type == JOYAXISMOTION:

                    # Is this axis on our xbox controller
                    if event.axis in self.AXISCONTROLMAP:

                        # Is this a y axis
                        yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
                        # Update the control value
                        self.updateControlValue(self.AXISCONTROLMAP[event.axis],
                                                self._sortOutAxisValue(event.value, yAxis))
                    # Is this axis a trigger
                    if event.axis in self.TRIGGERCONTROLMAP:

                        # Update the control value
                        self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis],
                                                self._sortOutTriggerValue(event.value))
                        
                # D pad
                elif event.type == JOYHATMOTION:

                    # Update control value
                    self.updateControlValue(self.XboxControls.DPAD, event.value)

                # Button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:

                    # Is this button on our xbox controller
                    if event.button in self.BUTTONCONTROLMAP:

                        # Update control value
                        self.updateControlValue(self.BUTTONCONTROLMAP[event.button],
                                                self._sortOutButtonValue(event.type))
        
    # Stops the controller
    def stop(self):
        self.running = False

    # Updates a specific value in the control dictionary
    def updateControlValue(self, control, value):
        #if the value has changed update it and call the callbacks
        if self.controlValues[control] != value:
            self.controlValues[control] = value
            self.doCallBacks(control, value)
    
    # Calls the call backs if necessary
    def doCallBacks(self, control, value):
        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

        #has a specific callback been setup?
        if control in self.controlCallbacks:
            self.controlCallbacks[control](value)
            
    #used to add a specific callback to a control
    def setupControlCallback(self, control, callbackFunction):
        # add callback to the dictionary
        self.controlCallbacks[control] = callbackFunction
                
    #scales the axis values, applies the deadzone
    def _sortOutAxisValue(self, value, yAxis = False):
        #invert yAxis
        if yAxis and self.invertYAxis: value = value * -1
        #scale the value
        value = value * self.scale
        #apply the deadzone
        if value < self.upperDeadzone and value > self.lowerDeadzone: value = 0
        return value

    #turns the trigger value into something sensible and scales it
    def _sortOutTriggerValue(self, value):
        #trigger goes -1 to 1 (-1 is off, 1 is full on, half is 0) - I want this to be 0 - 1
        value = max(0,(value + 1) / 2)
        #scale the value
        value = value * self.scale
        return value

    #turns the event type (up/down) into a value
    def _sortOutButtonValue(self, eventType):
        #if the button is down its 1, if the button is up its 0
        value = 1 if eventType == JOYBUTTONDOWN else 0
        return value
    
#tests
if __name__ == '__main__':
    frontLThruster = 1
    frontRThruster = 0
    midLThruster = 2
    midRThruster = 5
    backLThruster = 4
    backRThruster = 3
    cameraServo = 0
    clawRotateServo = 1
    clawServo = 2
    topSpeed = 200
    minSpeed = 100
    currClawDeg = 0
    currClawRotateDeg = 0
    rotateRight = False
    rotateLeft = False
    controls = Controls()
    controls.startThread()
    #generic call back
    def controlCallBack(xboxControlId, value):

        # make sure everything is an integer
        if isinstance(value, (int, float)):
            if value > 100:
                value = int(100)
            elif value < -100:
                value = int(-100)
            else:
                value = int(value)

        elif isinstance(value, tuple):
            value = (int(value[0]), int(value[1]))
        
        print(f"Control Id = {xboxControlId}, Value = {value}")
    
        """0 - x axis left thumb   (+1 is right, -1 is left)
        1 - y axis left thumb   (+1 is down, -1 is up)
        2 - x axis right thumb  (+1 is right, -1 is left)
        3 - y axis right thumb  (+1 is down, -1 is up)
        4 - right trigger
        5 - left trigger"""
        #robot thruster rotation
        #get left thumb and right thumb controls
        #move up, down, tilt, tilt
        
        # if (xboxControlId == 0):
        #     #tilt
        #     thrusterStrength = value*50+150
        #     reverseThrusterStrength = -1*value*50+150
        #     Controls.thrusterOn(midRThruster, reverseThrusterStrength)
        #     Controls.thrusterOn(midLThruster, thrusterStrength)
        # if (xboxControlId == 1):
        #     #move up and down
        #     thrusterStrength = value*50+150
        #     reverseThrusterStrength = -1*value*50+150
        #     Controls.thrusterOn(midRThruster, thrusterStrength)
        #     Controls.thrusterOn(midLThruster, thrusterStrength)
        
        #move front, back, side, side


        #Probably good one
        #thrusterStrength = (value + 100) / 2 + 100 # 100 to 200. 150 is stationart
        #reverseThrusterStrength = -1 * (thrusterStrength - 150) + 150
        thrusterStrength = (value + 100) / 2 + 100 # 100 to 200. 150 is stationart
        reverseThrusterStrength = -1 * (thrusterStrength - 150) + 150

        if xboxControlId == 0: # left-right movement  
            print(f"thrusterStrength: {thrusterStrength}, reverseThrusterStrength: {reverseThrusterStrength}")
            controls.thrusterOn(frontRThruster, int(thrusterStrength))
            controls.thrusterOn(frontLThruster, int(thrusterStrength))

            controls.thrusterOn(backRThruster, int(thrusterStrength))
            controls.thrusterOn(backLThruster, int(thrusterStrength))

        if xboxControlId == 1: # front-back movement
            print(f"thrusterStrength: {thrusterStrength}, reverseThrusterStrength: {reverseThrusterStrength}")
            controls.thrusterOn(frontRThruster, int(reverseThrusterStrength))
            controls.thrusterOn(frontLThruster, int(reverseThrusterStrength))

            controls.thrusterOn(backRThruster, int(reverseThrusterStrength))
            controls.thrusterOn(backLThruster, int(reverseThrusterStrength))


        if xboxControlId == 17: # up-down movement
            # thrusterStrength = 50 * value[1] + 150
            if value[1] > 0: # move up
                controls.thrusterOn(midLThruster, 200)    
                controls.thrusterOn(midRThruster, 200)
            elif value[0] < 0: # move down
                controls.thrusterOn(midLThruster, 100)    
                controls.thrusterOn(midRThruster, 100)

            if value[0] > 0: # tilting
                controls.thrusterOn(midLThruster, 200) # tilt to the right
            elif value[0] < 0: # tilt to the left
                controls.thrusterOn(midRThruster, 200)
            
            #reset, CHANGE THIS
            if value[0] == 0:
                controls.thrusterOn(midLThruster, 150)
                controls.thrusterOn(midRThruster, 150)
            if value[1] == 0:
                controls.thrusterOn(midLThruster, 150)
                controls.thrusterOn(midLThruster, 150)

        if xboxControlId == 2: # rotating to the left
            # thrusterStrength = (value + 100) / 4 + 150
            # reverseThrusterStrength = 150 - (value + 100) / 4  
            # |-> use if old controller

            thrusterStrength = value / 2 + 150
            reverseThrusterStrength = 150 - value / 2

            print(f"thrusterStrength: {thrusterStrength}, reverseThrusterStrength: {reverseThrusterStrength}")
            controls.thrusterOn(frontRThruster, int(thrusterStrength))
            controls.thrusterOn(backRThruster, int(thrusterStrength))

            controls.thrusterOn(backLThruster, int(reverseThrusterStrength))
            controls.thrusterOn(frontLThruster, int(reverseThrusterStrength))

        if xboxControlId == 5: # rotating to the right
            thrusterStrength = value / 2 + 150
            reverseThrusterStrength = 150 - value / 2

            print(f"thrusterStrength: {thrusterStrength}, reverseThrusterStrength: {reverseThrusterStrength}")
            controls.thrusterOn(frontLThruster, int(thrusterStrength))
            controls.thrusterOn(backLThruster, int(thrusterStrength))

            controls.thrusterOn(frontRThruster, int(reverseThrusterStrength))
            controls.thrusterOn(backRThruster, int(reverseThrusterStrength))


        if xboxControlId == 6: # close the claw
            controls.setClawDeg(clawServo, 89)

        if xboxControlId == 7: # opent the claw
            controls.setClawDeg(clawServo, 1)

        if xboxControlId == 8: # rotate the claw one way
            pass

        if xboxControlId == 9: # roate the claw the other way
            pass

        # if xboxControlId == [id of the middle 'X' button]:
        #     stop all the claw movements

        # if xboxControlId == [id of the middle left button]: 
        #     stop all the thrusters
        
        
    













    def moveSide(thrusterStrength):
        
        pass
    def moveFront(thrusterStrength):
        pass
    def moveUp(thrusterStrength):
        pass
    #specific callbacks for the left thumb (X & Y)
    def leftThumbX(xValue):
        pass
        # print(f"LX {xValue}")
    def leftThumbY(yValue):
        pass
        # print(f"LY {yValue}")

    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    xboxCont = XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    #setup the left thumb (X & Y) callbacks
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX, leftThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, leftThumbY)

    try:
        #start the controller
        xboxCont.start()
        print("xbox controller running")
        while True:
            time.sleep(1)

    #Ctrl C
    except KeyboardInterrupt:
        print("User cancelled")
    
    #error        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        
    finally:
        #stop the controller
        xboxCont.stop()


"""

100 back, forward is 200

front back left right left dpad

up and down
spin right and left left and right triggers
tilt left and right

claw opening
claw panning

camera panning





"""
