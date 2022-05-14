
# from queue import Queue
from tkinter import *
from pynput import keyboard
from dataclasses import dataclass


from controls import Controls
from botview import XboxViewer
import multiprocessing as mp
# from queue import Queue

from math import cos, sin, radians




@dataclass
class Thrusters:
    front_left = 4 
    front_right = 3

    mid_left = 1
    mid_right = 0

    back_left = 5
    back_right = 2

@dataclass
class Servos:
    claw = 2
    # Not in use
    # claw_rotate = 1
    # camera = 2


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

            # Not in use
            # "c": False,
            # "g": False,
            # "v": False,

            # "t": False,
            # "y": False,
            # "h": False,

            "q": False,
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
        self.thrust_cutter_key = ["q"]
        # self.clamp_rotate_action_keys = ["t", "y", "h"]
        # self.camera_action_keys = ["c", "g", "v"]

        self.clamp_angle = 0
        self.clamp_min_max_angle = [0, 90]

        self.clamp_rotate_angle = 0
        self.clamp_rotate_min_max_angle = [0, 90]

        self.cut_thrust = False
        self.cut_amount = 0.5

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
                # if self.cut_thrust:
                #     for modifier in ksms:
                #         modifier /= 2
            except KeyError:

                def determine_angle(pressed_key, current_angle, key_set, modify_amount, angle_range):
                    """
                    key_set in format [main, incrementer, decrementer]
                    angle_range in format [larger, smaller]
                    """

                    if pressed_key == key_set[0]:
                        to_max = angle_range[1] - current_angle
                        to_min = current_angle - angle_range[0]
                        if to_min < to_max:
                            return angle_range[1]
                        else:
                            return angle_range[0]
                    elif pressed_key == key_set[1]:
                        current_angle += modify_amount
                    else: # pressed_key == key_set[2]
                        current_angle -= modify_amount

                    if current_angle > angle_range[1]:
                        current_angle = angle_range[1]
                    elif current_angle < angle_range[0]:
                        current_angle = angle_range[0]

                    return current_angle

                if pressed_key in self.clamp_action_keys:
                    self.clamp_angle = determine_angle(pressed_key, self.clamp_angle, self.clamp_action_keys, 15, (0, 90))
                elif pressed_key in self.thrust_cutter_key:
                    if self.cut_thrust == False:
                        self.cut_thrust = True
                    else:
                        self.cut_thrust = False
                # elif pressed_key in self.camera_action_keys:
                #     self.camera_angle = determine_angle(pressed_key, self.camera_angle, self.camera_action_keys, 15, (0, 90))
                # elif pressed_key in self.clamp_rotate_action_keys:
                #     self.clamp_rotate_angle = determine_angle(pressed_key, self.clamp_rotate_angle, self.clamp_rotate_action_keys, 15, (0, 90))
            
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
        
        if self.cut_thrust:
            return [
                front_left_speed * self.cut_amount,
                front_right_speed* self.cut_amount,
                mid_left_speed* self.cut_amount,
                mid_right_speed* self.cut_amount,
                back_left_speed* self.cut_amount,
                back_right_speed* self.cut_amount,

                self.clamp_angle,
                self.camera_angle,
                self.clamp_rotate_angle,
            ]

        return [
            front_left_speed,
            front_right_speed,
            mid_left_speed,
            mid_right_speed,
            back_left_speed,
            back_right_speed,

            self.clamp_angle,
            self.camera_angle,
            self.clamp_rotate_angle,
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

    # print(f"{self.cut_thrust = }")
    print(f"\nfront left\t: {ts[0]}")
    print(f"front right\t: {ts[1]}")
    print(f"mid left\t: {ts[2]}")
    print(f"mid right\t: {ts[3]}")
    print(f"back left\t: {ts[4]}")
    print(f"back right\t: {ts[5]}")
    print(f"clamp angle\t: {ts[6]}")
    # print(f"camera r angle\t: {ts[8]}")
    # print(f"camera angle\t: {ts[7]}")

    ######### CALL THE CONTROLS HERE ###########
    controls.thrusterOn(Thrusters.front_left, ts[0])
    controls.thrusterOn(Thrusters.front_right, ts[1])
    controls.thrusterOn(Thrusters.mid_left, ts[2])
    controls.thrusterOn(Thrusters.mid_right, ts[3])
    controls.thrusterOn(Thrusters.back_left, ts[4])
    controls.thrusterOn(Thrusters.back_right, ts[5])
    
    controls.setClawDeg(Servos.claw, ts[6])
    # controls.setClawDeg(Servos.claw, ts[7])
    # controls.setClawDeg(Servos.claw_rotate, ts[8])



    


k = Keyhoard()
k.start()
controls = Controls()
controls.startThread()
# controls = 0


def create_view(pipe):
    root = Tk()
    root.title("Nemo Swim")
    root.geometry("500x500")


    viewer = XboxViewer(root, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)


    def checker():
        if not pipe.empty():
            ts = pipe.get()

            # 21 long, 15.5 wide
            # 98.569 degrees
            # 45 + asin(7.75 / 15) / acos(7.75 / 15)
            # 36.431 + 45 degrees




            front_left_torque = ts[0] * cos(radians(98.569 - 90))
            front_right_torque = -ts[1] * cos(radians(98.569 - 90))
            back_left_torque = ts[4] * cos(radians(90 - (36.431 + 45)))
            back_right_torque = -ts[5] * cos(radians(90 - (36.431 + 45)))

            front_left_y = ts[0] * sin(radians(45))
            front_right_y = ts[1] * sin(radians(135))
            back_left_y = ts[4] * sin(radians(135))
            back_right_y = ts[5] * sin(radians(45))

            front_left_x = round(ts[0] * cos(radians(45)), 3)
            front_right_x = round(ts[1] * cos(radians(135)), 3)
            back_left_x = round(ts[4] * cos(radians(135)), 3)
            back_right_x = round(ts[5] * cos(radians(45)),3)

            


            # print(f"{front_left_torque = }\t")
            # print(f"{front_right_torque = }\t")
            # print(f"{back_left_torque = }\t")
            # print(f"{back_right_torque = }\t")
            net_torque_z = round(front_left_torque + front_right_torque + back_left_torque + back_right_torque, 1)
            net_torque_y = 7.75 * ts[2] - 7.75 * ts[3]
            net_z = ts[2] + ts[3]
            net_y = round(front_left_y + front_right_y + back_left_y + back_right_y, 1)
            net_x = front_left_x + front_right_x + back_left_x + back_right_x

            # print(f"{net_torque_z = }")
            # print(f"{net_torque_y = }")
            # print(f"{net_z = }")
            # print(f"{net_y = }")
            # print(f"{net_x = }")

            # print(f"{front_left_y = }")
            # print(f"{front_right_y = }")
            # print(f"{back_left_y = }")
            # print(f"{back_right_y = }")
            # print(f"{front_left_x = }")
            # print(f"{front_right_x = }")
            # print(f"{back_left_x = }")
            # print(f"{back_right_x = }")
            # print()


            viewer.test3.edit((net_x / 150, net_y / 150))
            viewer.test5.edit(net_torque_z / 500)
            viewer.test7.edit(net_z / 100)


        viewer.after(10, checker)
    checker()

    root.mainloop()



def main(pipe):
    def on_press(key):
        try:
            char = key.char
            if char not in k.key_states.keys():
                print("Key not recognized...")
                return
            if not k.is_down(char):
                k.change_key_state(char, True)
                ts = k.thruster_speeds()
                show_thruster_speeds(ts=ts, controls=controls)
                # pipe.put(ts)


        except AttributeError:
            return

    def on_release(key):
        try:
            char = key.char
            if char not in k.key_states.keys():
                print("Key not recognized...")
                return
            if k.is_down(char):
                k.change_key_state(char, False)
                ts = k.thruster_speeds()
                show_thruster_speeds(ts=ts, controls=controls)
                # pipe.put(ts)


        except AttributeError:
            return


    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass



if __name__ == "__main__":
    pipe = mp.Queue()
    # if input("Open GUI(y/n): ").lower() == "y":
        # gui_thread = mp.Process(target=create_view, args=(pipe,))
        # keyboard_thread = mp.Process(target=main, args=(pipe,))

        # gui_thread.start()
        # keyboard_thread.start()
        
        # keyboard_thread.join()
        # gui_thread.join()
    # else:
    main(pipe)