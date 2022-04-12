from pynput import keyboard
from controls import Controls
from sys import exit

class KeyboardInput:
    def __init__(self):
        pass
    def startKeyboardReading(self): #start keyboard reading
        pass

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

currClawDeg = 0 # just the claw's clamp thingy
currClawRotateDeg = 0 # whole claw thingy
currCameraServoDeg = 0

rotateRight = False
rotateLeft = False
controls = Controls()
controls.startThread()

is_down = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "j": False,
    "l": False,

    "i": False,
    "k": False,
    "u": False,
    "o": False,

    "e": False,
}

claw_is_clamped = False

delta_speed = { # _____ : [front left, front right, back left, back right]
    "w": [50, 50, 50, 50], #front
    "a": [-50, 50, 50, -50], #left
    "s": [-50, -50, -50, -50], #back
    "d": [50, -50, -50, 50], #right
    "j": [-50, 50, -50, 50], #rotate
    "l": [50, -50, 50, -50], #rotate

    "i": [50, 50], #
    "k": [-50, -50],
    "u": [-50, 50],
    "o":[50, -50]
}

accepted_chars = ["w", "a", "s", "d", "j", "l", "i", "k", "u", "o", "e", "1", "2", "r", "f", "x", "3", "4", "c", "v"]
wasdjl_keys = ["w", "a", "s", "d", "j", "l"]
ikuo_keys = ["i", "k", "u", "o"]

def all_wasdjl_downs():
    downs = []
    for char, value in is_down.items():
        if value == True:
            if char in wasdjl_keys:
                downs.append(char)

    return downs

def all_ikuo_downs():
    downs = []
    for char, value in is_down.items():
        if value == True:
            if char in ikuo_keys:
                downs.append(char)
    # print(is_down)
    return downs

def power():
    # global claw_is_clamped
    frontLThrusterSpeed = 0
    frontRThrusterSpeed = 0
    backLThrusterSpeed = 0
    backRThrusterSpeed = 0
    midLThrusterSpeed = 0
    midRThrusterSpeed = 0
    for char in all_wasdjl_downs():
        frontLThrusterSpeed += delta_speed[char][0]
        frontRThrusterSpeed += delta_speed[char][1]
        backLThrusterSpeed += delta_speed[char][2]
        backRThrusterSpeed += delta_speed[char][3]
    
    for char in all_ikuo_downs():
        midLThrusterSpeed += delta_speed[char][0]
        midRThrusterSpeed += delta_speed[char][1]

    # Get the average thruster speeds
    l = len(all_wasdjl_downs())
    if l >= 2:
        frontLThrusterSpeed = round(frontLThrusterSpeed / l)
        frontRThrusterSpeed = round(frontRThrusterSpeed / l)
        backLThrusterSpeed = round(backLThrusterSpeed / l)
        backRThrusterSpeed = round(backRThrusterSpeed / l)


    if len(all_ikuo_downs()) >= 2:
        midLThrusterSpeed = int(midLThrusterSpeed / 2)
        midRThrusterSpeed = int(midRThrusterSpeed / 2)

    print(f"{frontLThrusterSpeed = }")
    print(f"{frontRThrusterSpeed = }")
    print(f"{backLThrusterSpeed = }")
    print(f"{backRThrusterSpeed = }")

    print(f"{midLThrusterSpeed = }")
    print(f"{midRThrusterSpeed = }")
    print(f"{currClawRotateDeg = }")
    print(f"{currCameraServoDeg = }")
    
    controls.thrusterOn(frontLThruster, frontLThrusterSpeed)
    controls.thrusterOn(frontRThruster, frontRThrusterSpeed)
    controls.thrusterOn(backLThruster, backLThrusterSpeed)
    controls.thrusterOn(backRThruster, backRThrusterSpeed)
    controls.thrusterOn(midLThruster, midLThrusterSpeed)
    controls.thrusterOn(midRThruster, midRThrusterSpeed)

    #controls.setClawDeg(clawRotateServo, currClawRotateDeg)
    #controls.setClawDeg(cameraServo, currCameraServoDeg)






def on_press(key):
    global currClawRotateDeg
    global currCameraServoDeg
    # Check if key type is valid
    try:
        char = key.char
        # print(type(char))
        # print(char)
        # print(char == "1")
    except AttributeError:
        # print(f"Special key '{key}' pressed")
        return

    if char in is_down.keys():
        if is_down[char] == True:
            # print("Skipping because already on")
            return

    if char in accepted_chars:
        is_down[char] = True
    else:
        return
    if char == "x":
        controls.thrusterOn(frontLThruster, 0)
        controls.thrusterOn(frontRThruster, 0)
        controls.thrusterOn(backLThruster, 0)
        controls.thrusterOn(backRThruster, 0)
        controls.thrusterOn(midLThruster, 0)
        controls.thrusterOn(midRThruster, 0)

    elif char == "1":
        if currClawRotateDeg - 10 < 0:
            currClawRotateDeg = 0
        else:
            currClawRotateDeg -= 10
        controls.setClawDeg(clawRotateServo, currClawRotateDeg)

    elif char == "2":
        if currClawRotateDeg + 10 > 180:
            currClawRotateDeg = 180
        else:
            currClawRotateDeg += 10
        controls.setClawDeg(clawRotateServo, currClawRotateDeg)

    elif char == "3":
        currClawRotateDeg = 0
        controls.setClawDeg(clawRotateServo, 0)
    
    elif char == "4":
        currClawRotateDeg = 90
        controls.setClawDeg(clawRotateServo, 90)



    elif char == "r":
        if currCameraServoDeg - 10 < 0:
            currCameraServoDeg = 0
        else:
            currCameraServoDeg -= 10
        controls.setClawDeg(cameraServo, currCameraServoDeg)

    elif char == "f":
        if currCameraServoDeg + 10 > 70:
            currCameraServoDeg = 70
        else:
            currCameraServoDeg += 10
        controls.setClawDeg(cameraServo, currCameraServoDeg)
    elif char == "c":
        currCameraServoDeg = 0
        controls.setClawDeg(cameraServo, 0)

    elif char == "v":
        currCameraServoDeg = 70
        controls.setClawDeg(cameraServo, 70)


    # controls.setClawDeg(clawRotateServo, currClawRotateDeg)
        

    power()



def on_release(key):
    global claw_is_clamped
    # Check if key type is valid
    try:
        char = key.char
        # print(char)
    except AttributeError:
        print(f"Special key '{key}' pressed")
        return

    if char in is_down.keys():
        if is_down[char] == False:
            # print("Skipping because already off")
            return

    if char in accepted_chars:
        is_down[char] = False

    if char == "e":
        if claw_is_clamped:
            print("unclamping")
            controls.setClawDeg(clawServo, 89)
            claw_is_clamped = False
        else:
            print("clamping")
            controls.setClawDeg(clawServo, 1)
            claw_is_clamped = True

    power()


def main():
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    main()