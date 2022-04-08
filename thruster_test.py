from controls import Controls
from time import sleep

controls = Controls()
controls.startThread()

for i in range (100, 151, 10):
    controls.thrusterOn(1, i)
    sleep(2)
    
