from dataclasses import dataclass
from tkinter import Canvas, Frame, CENTER, Tk
from typing import Union


@dataclass
class State():
    """
    A struct for storing instructions for displaying the controls in a GUI
    
    cid -> control id
    
    relpos -> position

    displacement (for 2-axis controls) -> which way the control has been shifted
    in x, y direction
    
    activation -> For the triggers, any number between 1 and 0. Binary for normal
    buttons
    """
    CID: int
    RELPOS: tuple[float, float]
    RADIUS: float = 10
    disp: tuple[float, float] = None
    activation: float = 0

class ControlStates(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.bounds = (500, 500)
        self.c = Canvas(self, bg="white", width=self.bounds[0], height=self.bounds[1])
        self.c.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controlstates = { # Control ID : Control State
            6: State(6, (0.76, 0.36335)),
            7: State(7, (0.82889, 0.27019)),
            8: State(8, (0.68889, 0.27019)),
            9: State(9, (0.76, 0.18012)),

            10: State(10, (0.76, 0.046583)),
            11: State(11, (0.24, 0.46583)),

            12: State(12, (0.42667, 0.27019)),
            13: State(13, (0.57333, 0.27019)),
            14: State(14, (0.5, 0.10248)),

            17: State(17, (0.36667, 0.50311), disp=(0, 0)),
        }

        self.buttons = ["6", "7", "8", "9", "10", "11", "12", "13", "14", "17"]
        self.analogs = []

    def show_control(self, cid):
        pos = self.pos(cid)
        rad = self.radius(cid)

        x0 = pos[0] - rad
        y0 = pos[1] - rad
        x1 = pos[0] + rad
        y1 = pos[1] + rad
        self.c.create_oval(x0, y0, x1, y1)

    

    
    def change_state(self, cid: str, new_val: Union[tuple[float, float], float]):
        if self.control_type(cid) == "button":
            self.controlstates[cid].activation = new_val

        elif self.control_type(cid) == "analog":
            pass
    
    
    # Behaves like a property
    def control_type(self, cid):
        if cid in self.buttons:
            return "button"
        elif cid in self.analogs:
            return "analog"
    
    @property
    def pos(self, cid):
        max_width = 500
        max_height = 500
        x = max_width * self.controlstates[cid].RELPOS[0]
        y = max_height * self.controlstates[cid].RELPOS[1]
        return (x, y)
    
    @property
    def radius(self, cid):
        return self.controlstates[cid].RADIUS


    
        
root = Tk()
root.geometry("500x500")
root.update()




viewer = XboxViewer(root, bg="purple", width=500, height=500)
viewer.pack()

root.mainloop()


    


    


