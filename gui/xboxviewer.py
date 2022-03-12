from dataclasses import dataclass
from tkinter import Canvas
from typing import Union




class XboxViewer():
    def __init__(self):
        self.contstate = self.XboxControls()
    
    class XboxControls():

        @dataclass
        class Info():
            """
            A struct for storing instructions for displaying the controls in a GUI
            
            cid -> control id
            
            relpos -> position

            displacement (for 2-axis controls) -> which way the control has been shifted
            in x, y direction
            
            activation -> For the triggers, any number between 1 and 0. Binary for normal
            buttons
            """
            cid: int
            relpos: tuple[float, float]

            radius: float = 10
            disp: tuple[float, float] = None
            activation: float = 0

        def __init__(self):
            self.controls


            self.A = self.Info(6, (0.76, 0.36335))
            self.B = self.Info(7, (0.82889, 0.27019))
            self.X = self.Info(8, (0.68889, 0.27019))
            self.Y = self.Info(9, (0.76, 0.18012))

                # B means bumper
            self.LB = self.Info(10, (0.76, 0.046583))
            self.RB = self.Info(11, (0.24, 0.46583))

            self.BACK = self.Info(12, (0.42667, 0.27019))
            self.START = self.Info(13, (0.57333, 0.27019))
            self.XBOX = self.Info(14, (0.5, 0.10248))

                # LEFTTHUMB = self.Info(15 )
                # RIGHTTHUMB = self.Info(16)
            self.DPAD = self.Info(17, (0.36667, 0.50311), disp=(0, 0))

    



viewer = XboxViewer()
print(viewer.controls.START)

    


    


