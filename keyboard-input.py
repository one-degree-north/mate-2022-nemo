import pynput

def on_press(key):
    if isinstance(key, pynput.keyboard.KeyCode):
        print(f"key = {key.char}")
    else:
        print(f"key={key}")
    pass

def on_release(key):
    if isinstance(key, pynput.keyboard.KeyCode):
        pass
    else:
        pass
    pass

def main():
    keyboardListener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()
    while True:
        pass

if __name__ == "__main__":
    main()