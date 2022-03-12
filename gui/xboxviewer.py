from dataclasses import dataclass
from tkinter import Canvas
from typing import Union




class XboxViewer(Canvas):

    class XboxControls():
        
        @dataclass
        class Info():
            """
            A struct for storing how the controls are displayed in the GUI
            cid -> control id
            pos -> position
            displacement (for 2-axis controls) -> which way the control has been shifted
            in x, y direction
            activation -> For the triggers, any number between 1 and 0. Binary for normal
            buttons
            """
            cid: int
            pos: tuple[float, float]
            displacement: tuple[float, float] = None
            activation: float = 0
        
        
        # Max min height -> 78, 400
        # Max min width -> 26, 476

        # LTHUMBX = Info(0, ())
        # LTHUMBY = Info(1)
        # RTHUMBX = Info(2)
        # RTHUMBY = Info(3)
        RTRIGGER = Info(4,)
        LTRIGGER = Info(5,)

        A = Info(6, (368, 195))
        B = Info(7, (399, 165))
        X = Info(8, (336, 165))
        Y = Info(9, (368, 136))

        # B means bumper
        LB = Info(10, (368, 93))
        RB = Info(11, (134, 93))

        BACK = Info(12, (218, 165))
        START = Info(13, (284, 165))
        XBOX = Info(14, (251, 111))

        # LEFTTHUMB = Info(15 )
        # RIGHTTHUMB = Info(16)
        DPAD = Info(17, (191, 240), disp=(0, 0))

    


    


