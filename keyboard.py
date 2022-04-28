
from pynput import keyboard
from dataclasses import dataclass

class Keyhoard():

    @dataclass
    class Thrusters:
        front_left = 1
        front_right = 0

        mid_left = 2
        mid_right = 5

        back_left = 4
        back_right = 3


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

        self.claw_is_clamped = False

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
            ksms = self.speed_modifiers[pressed_key] # key speed modifier set
            if pressed_key in self.move_action_keys or pressed_key in self.rotate_action_keys:
                
                # print("incrementing horiz divisor")
                horiz_divisor += 1
                front_left_speed += ksms[0]
                front_right_speed += ksms[1]
                back_left_speed += ksms[2]
                back_right_speed += ksms[3]

            elif pressed_key in self.height_action_keys or pressed_key in self.tilt_action_keys:
                # print("incrementing vert divisor")
                vert_divisor += 1
                mid_left_speed += ksms[0]
                mid_right_speed += ksms[1]

        # probably not the best way to do this
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

def show_thruster_speeds(ts):

    print(f"\nfront left\t: {ts[0]}")
    print(f"front right\t: {ts[1]}")
    print(f"mid left\t: {ts[2]}")
    print(f"mid right\t: {ts[3]}")
    print(f"back left\t: {ts[4]}")
    print(f"back right\t: {ts[5]}")



k = Keyhoard()
k.start()


def on_press(key):
    try:
        char = key.char
        if char not in k.key_states.keys():
            print("Key not recognized...")
            return
        if not k.is_down(char):
            k.change_key_state(char, True)
            ts = k.thruster_speeds()
            show_thruster_speeds(ts=ts)


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
            show_thruster_speeds(ts=ts)

    except AttributeError:
        return

    



def main():
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    main()