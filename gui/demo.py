"""
Template code for communication between controller/controller.py
and gui/xboxviewer.py
"""

import multiprocessing as mp

from time import sleep
from random import randint


def one(q):
    """
    Queue checker

    If q.get() is recognized, call a function
    according to its contents
    """
    while True:
        thingy = q.get()
        print(thingy)
        if thingy == 1:
            
            print("Found one!")


def two(q):
    """
    This simulates controller input being
    added to a queue
    """
    while True:
        r = randint(1,2)
        q.put(r)
        sleep(1)

if __name__ == "__main__":
    q = mp.Queue(1)

    t1 = mp.Process(target=one, args=(q,))
    t2 = mp.Process(target=two, args=(q,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

