
# from queue import Queue
from tkinter import *
from pynput import keyboard
from dataclasses import dataclass
from controls import Controls
from botview import XboxViewer
import multiprocessing as mp
from multiprocessing import Queue


@dataclass
class Thrusters:
    front_left = 1
    front_right = 0

    mid_left = 2
    mid_right = 5

    back_left = 4
    back_right = 3

class Keyhoard():
    def __init__(self):
        self.key_states = {
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
            "r": False,
            "f": False,

            "c": False,
            "g": False,
            "v": False,
        }

        self.speed_modifiers = {
            "w": [50, 50, 50, 50], #front
            "a": [-50, 50, 50, -50], #left
            "s": [-50, -50, -50, -50], #back
            "d": [50, -50, -50, 50], #right

            "j": [-50, 50, -50, 50], #rotate
            "l": [50, -50, 50, -50], #rotate

            "i": [50, 50], 
            "k": [-50, -50],
            "u": [-50, 50],
            "o":[50, -50]
        }

        self.move_action_keys = ["w", "a", "s", "d"]
        self.height_action_keys = ["i", "k"]
        self.tilt_action_keys = ["u", "o"]
        self.rotate_action_keys = ["j", "l"]
        self.clamp_action_keys = ["e", "r", "f"]
        self.camera_action_keys = ["c", "g", "v"]

        self.clamp_angle = 0
        self.clamp_min_max_angle = [0, 90]

        self.claw_is_clamped = False

        self.camera_angle = 0
        self.camera_min_max_angle = [0, 90]

        self.print_values = True

    def start(self):
        pass

    def pressed_keys(self):
        output_keys = []
        for key, is_pressed in self.key_states.items():
            if is_pressed:
                output_keys.append(key)
        return output_keys

    def thruster_speeds(self):
        front_left_speed = 0
        front_right_speed = 0
        mid_left_speed = 0
        mid_right_speed = 0
        back_left_speed = 0
        back_right_speed = 0

        horiz_divisor = 0
        vert_divisor = 0

        for pressed_key in self.pressed_keys():
            try:
                ksms = self.speed_modifiers[pressed_key] # key speed modifier set
            except KeyError:
                if pressed_key in self.clamp_action_keys:
                    if pressed_key == "e":
                        to_max = self.clamp_min_max_angle[1] - self.clamp_angle
                        to_min = self.clamp_angle - self.clamp_min_max_angle[0]
                        if to_min < to_max:
                            self.clamp_angle = self.clamp_min_max_angle[1]
                        else:
                            self.clamp_angle = self.clamp_min_max_angle[0]
                    elif pressed_key == "r":
                        self.clamp_angle += 15
                        self.clamp_angle = self.clamp_min_max_angle[1] if self.clamp_angle > self.clamp_min_max_angle[1] else self.clamp_angle
                    elif pressed_key == "f":
                        self.clamp_angle -= 15
                        self.clamp_angle = self.clamp_min_max_angle[0] if self.clamp_angle < self.clamp_min_max_angle[0] else self.clamp_angle

                elif pressed_key in self.camera_action_keys:
                    if pressed_key == "c":
                        to_max = self.camera_min_max_angle[1] - self.camera_angle
                        to_min = self.camera_angle - self.camera_min_max_angle[0]
                        if to_min < to_max:
                            self.camera_angle = self.camera_min_max_angle[1]
                        else:
                            self.camera_angle = self.camera_min_max_angle[0]
                    elif pressed_key == "g":
                        self.camera_angle += 15
                        self.camera_angle = self.camera_min_max_angle[1] if self.camera_angle > self.camera_min_max_angle[1] else self.camera_angle
                    elif pressed_key == "v":
                        self.camera_angle -= 15
                        self.camera_angle = self.camera_min_max_angle[0] if self.camera_angle < self.camera_min_max_angle[0] else self.camera_angle
            
            
            if pressed_key in self.move_action_keys or pressed_key in self.rotate_action_keys:
                horiz_divisor += 1
                front_left_speed += ksms[0]
                front_right_speed += ksms[1]
                back_left_speed += ksms[2]
                back_right_speed += ksms[3]

            elif pressed_key in self.height_action_keys or pressed_key in self.tilt_action_keys:
                vert_divisor += 1
                mid_left_speed += ksms[0]
                mid_right_speed += ksms[1]

        if horiz_divisor == 0:
            horiz_divisor = 1
        if vert_divisor == 0:
            vert_divisor = 1

        front_left_speed = front_left_speed / horiz_divisor
        front_right_speed = front_right_speed / horiz_divisor
        back_left_speed = back_left_speed / horiz_divisor
        back_right_speed = back_right_speed / horiz_divisor

        mid_left_speed = mid_left_speed / vert_divisor
        mid_right_speed = mid_right_speed / vert_divisor

        return [
            front_left_speed,
            front_right_speed,
            mid_left_speed,
            mid_right_speed,
            back_left_speed,
            back_right_speed,

            self.clamp_angle,
            self.camera_angle,
        ]

    def change_key_state(self, key, new_state):
        if key in self.key_states:
            self.key_states[key] = new_state
        else:
            print("key is not recognized")

    def is_down(self, key):
        if self.key_states[key] == True:
            return True
        return False

def show_thruster_speeds(ts, controls: Controls, gui: Tk = None):

    # print(f"\nfront left\t: {ts[0]}")
    # print(f"front right\t: {ts[1]}")
    # print(f"mid left\t: {ts[2]}")
    # print(f"mid right\t: {ts[3]}")
    # print(f"back left\t: {ts[4]}")
    # print(f"back right\t: {ts[5]}")
    # print(f"clamp angle\t: {ts[6]}")
    # print(f"camera angle\t: {ts[7]}")


    ######### CALL THE CONTROLS HERE ###########
    # controls.thrusterOn(Thrusters.front_left, ts[0])
    # controls.thrusterOn(Thrusters.front_right, ts[1])
    # controls.thrusterOn(Thrusters.mid_left, ts[2])
    # controls.thrusterOn(Thrusters.mid_right, ts[3])
    # controls.thrusterOn(Thrusters.back_left, ts[4])
    # controls.thrusterOn(Thrusters.back_right, ts[5])

    ######### ADJUSTING THE GUI ##########
    pass


    


k = Keyhoard()
k.start()
pipe = Queue()

def create_view():
    global pipe
    root = Tk()
    root.title("XBox Viewer")
    root.geometry("500x500")


    viewer = XboxViewer(root, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)


    def checker():
        print("checking")
        if not pipe.empty():
            print(pipe.get())

        viewer.after(1000, checker)
    checker()

    root.mainloop()

def on_press(key):
    global pipe
    try:
        char = key.char
        if char not in k.key_states.keys():
            print("Key not recognized...")
            return
        if not k.is_down(char):
            k.change_key_state(char, True)
            ts = k.thruster_speeds()
            show_thruster_speeds(ts=ts, controls=None)
            pipe.put("Hello")

    except AttributeError:
        return

def on_release(key):
    global pipe
    try:
        char = key.char
        if char not in k.key_states.keys():
            print("Key not recognized...")
            return
        if k.is_down(char):
            k.change_key_state(char, False)
            ts = k.thruster_speeds()
            show_thruster_speeds(ts=ts, controls=None)
            pipe.put("Hello")

    except AttributeError:
        return

def main():
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    # pipe.put("Hello")

    print("\n"*10)

    keyboard_thread = mp.Process(target=main)
    gui_thread = mp.Process(target=create_view)

    gui_thread.start()
    keyboard_thread.start()
    
    keyboard_thread.join()
    gui_thread.join()