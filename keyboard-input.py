from ftplib import all_errors
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
    "w": False,
    "a": False,
    "s": False,
    "d": False,
}

delta_speed = { # _____ : [front left, front right, back left, back right]
    "w": [50, 50, 50, 50],
    "a": [-50, 50, 50, -50],
    "s": [-50, -50, -50, -50],
    "d": [50, -50, -50, 50],
}

accepted_chars = ["w", "a", "s", "d"]

def all_downs():
    downs = []
    for char, value in is_down.items():
        if value == True:
            downs.append(char)

    return downs

def power():
    frontLThrusterSpeed = 0
    frontRThrusterSpeed = 0
    backLThrusterSpeed = 0
    backRThrusterSpeed = 0
    for char in all_downs():
        frontLThrusterSpeed += delta_speed[char][0]
        frontRThrusterSpeed += delta_speed[char][1]
        backLThrusterSpeed += delta_speed[char][2]
        backRThrusterSpeed += delta_speed[char][3]

    # Get the average thruster speeds
    l = len(all_downs())
    frontLThrusterSpeed = round(frontLThrusterSpeed / l)
    frontRThrusterSpeed = round(frontRThrusterSpeed / l)
    backLThrusterSpeed = round(backLThrusterSpeed / l)
    backRThrusterSpeed = round(backRThrusterSpeed / l)

    print(f"{frontLThrusterSpeed = }")
    print(f"{frontRThrusterSpeed = }")
    print(f"{backLThrusterSpeed = }")
    print(f"{backRThrusterSpeed = }")
    
    # controls.thrusterOn(frontLThruster, frontLThrusterSpeed)
    # controls.thrusterOn(frontRThruster, frontRThrusterSpeed)
    # controls.thrusterOn(backLThruster, backLThrusterSpeed)
    # controls.thrusterOn(backRThruster, backRThrusterSpeed)

# controls = Controls()
# controls.startThread()




def on_press(key):
    # Check if key type is valid
    try:
        char = key.char
        # print(char)
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

    power()



def on_release(key):
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

    # power()


def main():
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    main()