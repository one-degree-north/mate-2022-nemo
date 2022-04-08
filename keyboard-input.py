from pynput import keyboard
from controls import Controls
from sys import exit

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

is_down = {
    "w": False
}

# controls = Controls()
# controls.startThread()




def on_press(key):
    # Check if key type is valid
    try:
        # print(key.char)
        pass
    except AttributeError:
        print(f"Special key '{key}' pressed")
        return

    speed = 200
    reverse_speed = 300 - speed
    try:
        char = key.char
    except:
        exit()
    
    if char == "w" and not is_down["w"]:
        # controls.thrusterOn(frontRThruster, speed)
        # controls.thrusterOn(fwwrontLThruster, speed)
        # controls.thrusterOn(backRThruster, speed)
        # controls.thrusterOn(backLThruster, speed)
        print("yay1")
        is_down["w"] = True
        pass

    elif char == "s":
        # controls.thrusterOn(frontRThruster, reverse_speed)
        # controls.thrusterOn(frontLThruster, reverse_speed)
        # controls.thrusterOn(backRThruster, reverse_speed)
        # controls.thrusterOn(backLThruster, reverse_speed)
        # print("yay2")
        pass
    
    elif char == "a":
        pass

    elif char == "a":
        pass
    

def on_release(key):
    # Check if key type is valid
    try:
        print(key.char)
    except AttributeError:
        print(f"Special key '{key}' released")
        return

    try:
        char = key.char
    except:
        exit()

    if char == "w" and is_down["w"]:
        is_down["w"] = False


def main():
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    main()