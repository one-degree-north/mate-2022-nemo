"""
Template for a communication with a tkinter 'while loop'
"""



from tkinter import *
from random import randint
from time import sleep

import multiprocessing, queue

q = queue.Queue()

def gui():
    root = Tk()
    root.geometry("500x500")
    root.update()

    l = Label(root, text="Off")
    l.pack()

    def switch_loop(l):
        # trigger = get stuff from queue
        if randint(1,2) == 1:
            print(1)
            # print("\tFlicking...")
            if l.cget("text") == "On":
                l.configure(text="Off")
            else:
                l.configure(text="On")
        else:
            print(2)
        l.after(1000, switch_loop, l)

    switch_loop(l)

    root.mainloop()
    
def looper():
    count = 0
    while True:
        print(count)
        count += 1
        sleep(1)


if __name__ == "__main__":
    t1 = multiprocessing.Process(target=gui)
    t2 = multiprocessing.Process(target=looper)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


