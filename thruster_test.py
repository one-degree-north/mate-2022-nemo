from controls import Controls
from time import sleep

controls = Controls()
controls.startThread()

for i in range (100, 151, 10):
    controls.thrusterOn(1, i)
    sleep(2)
    

"""
id 0 and 1 are giving 150 at negative y and x positions

when release, 2 is 175 positive, 125 for negative 

need to handle tuple 
"""