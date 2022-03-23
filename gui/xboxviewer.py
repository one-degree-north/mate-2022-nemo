from dataclasses import dataclass
from tkinter import Canvas, Frame, CENTER, Tk
from typing import Union
from time import sleep
from math import floor


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

@dataclass
class Color():
    active = "#BBCEFF"
    passive = "#004AFF"

class XboxViewer(Frame):

    def __init__(self, parent, q, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent: Tk = parent
        # Start the canvas
        self.relative_canvas_width, self.relative_canvas_height = 0.5, 0.5
        self.c = Canvas(self, bg="white", width=500, height=500)
        self.c.bind("<Configure>", self.move)
        self.c.place(relx=0.5, rely=0.5, relwidth=self.relative_canvas_width, relheight=self.relative_canvas_height, anchor=CENTER)
        # Put controls onto the canvas
        self.controlstates = { # Control ID : Control State
            "6": State(6, (0.5, 0.66667)),
            "7": State(7, (0.66667, 0.5)),
            "8": State(8, (0.33333, 0.5)),
            "9": State(9, (0.5, 0.33333)),
        }

        self.canvas_item_ids = {} # Control ID : Canvas Item ID 

        self.buttons = ["6", "7", "8", "9", "10", "11", "12", "13", "14", "17"]
        self.analogs = []

        for control in self.controlstates.keys():
            self.show_control(control)

        sleep(1)

        def checker():
            thingy = q.get()
            print("checking...")
            
            if thingy[0] == "6":
                print("switching...")
                if thingy[1] == 1:
                    self.change_state("6", new_val=1)
                elif thingy[1] == 0:
                    self.change_state("6", new_val=0)
            
            self.after(1, checker)

        checker()
        print("checker passed")
        # q.put("done")
        

    def show_control(self, cid, is_active=False):
        if cid in self.controlstates:
            pos = self.pos(cid)
            rad = self.radius(cid)
            self.c.update()
            self.c.update_idletasks()

            print(f"{pos = }, {rad = }")
            # print(f"{self.c.winfo_width() = }, {self.c.winfo_height() = }")

            x0 = pos[0] - rad
            y0 = pos[1] - rad
            x1 = pos[0] + rad
            y1 = pos[1] + rad

            fill = ""
            if is_active:
                fill = Color.active
            else:
                fill = Color.passive

            canvas_item_id: str = self.c.create_oval(x0, y0, x1, y1, fill=fill)
            self.canvas_item_ids[cid] = canvas_item_id


    

    
    def change_state(self, cid: str, new_val: Union[tuple[float, float], float]=None, new_pos: tuple[float, float]=None):
        # print("doing")
        if cid in self.canvas_item_ids.keys():
            item_id = self.canvas_item_ids[cid]

            if new_pos != None:
                x0 = new_pos[0] - 10
                y0 = new_pos[1] - 10
                x1 = new_pos[0] + 10
                y1 = new_pos[1] + 10
                # self.c.moveto(item_id, new_pos[0], new_pos[1]) <- this doesn't align stuff correctly for some odd reason
                self.c.coords(item_id, x0, y0, x1, y1)
            
            if self.control_type(cid) == "button":
                # print("controller is a button")
                if self.controlstates[cid].activation != new_val and self.controlstates[cid].activation != None:
                    self.controlstates[cid].activation = new_val
                    
                    if new_val == 0:
                        self.c.itemconfig(item_id, fill=Color.passive)
                    elif new_val == 1:
                        self.c.itemconfig(item_id, fill=Color.active)


            elif self.control_type(cid) == "analog":
                pass

        else:
            print("cid not found")

        # self.after(1000, self.change_state)

    

    def move(self, event):

        def adjust_control_pos():
            pass

        # print("moving")
        print(f"{self.canvas_size = }")
        for control in self.canvas_item_ids.keys():
            new_x, new_y = self.canvas_size
            new_x *= self.controlstates[control].RELPOS[0]
            new_y *= self.controlstates[control].RELPOS[1]
            v = 0
            if self.canvas_size[0] > 500:
                v = 1
            self.change_state(cid=control, new_pos=(new_x, new_y), new_val=v)

    
    @property
    def canvas_size(self) -> tuple[int, int]:
        self.parent.update()
        self.parent.update_idletasks()
        
        width = floor(self.parent.winfo_width() * self.relative_canvas_width)
        height = floor(self.parent.winfo_height() * self.relative_canvas_height)

        return (width, height)

    def control_type(self, cid):
        if cid in self.buttons:
            return "button"
        elif cid in self.analogs:
            return "analog"
    

    def pos(self, cid):
        max_width = 500
        max_height = 500
        x = max_width * self.controlstates[cid].RELPOS[0]
        y = max_height * self.controlstates[cid].RELPOS[1]

        return (x, y)
    

    def radius(self, cid):
        return self.controlstates[cid].RADIUS



if __name__ == "__main__":   
    root = Tk()
    root.geometry("500x500")
    root.update()




    viewer = XboxViewer(root, bg="lightgrey", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

    root.mainloop()






    


    


