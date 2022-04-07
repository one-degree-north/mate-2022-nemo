from dataclasses import dataclass
from tkinter import Canvas, Frame, CENTER, Tk

import queue
from typing import Union
from time import sleep
from math import floor, sin, cos





class XboxViewer(Frame):

    class Control(object):
        ctrls = []
        ctrl_ids = {} # Cid: canvas item id
        
        def __init__(self, frame_in, canvas, cid, relpos, radius, activation=0):
            self.frame_in: Frame = frame_in
            self.canvas: Canvas = canvas
            self.cid = cid
            self.relpos = relpos
            self.radius = radius
            self.activation = activation

            self.palette = {}

            self.ctrls.append(self)

        def create(self):
            cc = self.corner_coords()
            self.canvas_id = self.canvas.create_oval(cc[0], cc[1], cc[2], cc[3], width=2, fill=self.dip_paintbrush(), outline=self.palette[self.cid]["off"]) 

        def edit(self, val):
            if self.activation != val:
                print("changing")
                self.activation = val
                self.canvas.itemconfig(self.canvas_id, fill=self.dip_paintbrush())

        def corner_coords(self):
            x0 = self.rel2abspos()[0] - self.radius
            x1 = self.rel2abspos()[0] + self.radius
            y0 = self.rel2abspos()[1] - self.radius
            y1 = self.rel2abspos()[1] + self.radius
            return (x0, y0, x1, y1)

        def rel2abspos(self):
            x = self.frame_in.parent.winfo_width() * self.relpos[0]
            y = self.frame_in.parent.winfo_height() * self.relpos[1]
            return (x, y)

        def dip_paintbrush(self):
            return "white"

        def shift(self):
            cc = self.corner_coords()
            self.canvas.coords(self.canvas_id, cc[0], cc[1], cc[2], cc[3])

        @classmethod
        def fetch_cids(cls):
            return cls.ctrl_ids
        
        @classmethod
        def fetch_all_controls(cls):
            return cls.ctrls

    class ABXY(Control):
        def __init__(self, frame_in, canvas, cid, relpos, radius, activation):
            super().__init__(frame_in, canvas, cid, relpos, radius, activation)
            self.palette = {
                "6": {"on": "#a9ff94", "off": "#00b315"},
                "7": {"on": "#ff9494", "off": "#b30000"},
                "8": {"on": "#949bff", "off": "#004eb3"},
                "9": {"on": "#fdff94", "off": "#b0b300"},
            }

        def dip_paintbrush(self):
            paint = self.palette[self.cid]["on"] if self.activation == 1 else self.palette[self.cid]["off"]
            return paint

    class Joystick(Control):
        def __init__(self, frame_in, canvas, cid: tuple, relpos, radius, activation: tuple):
            """
            cid and radius are tuples
            main in front
            """
            super().__init__(frame_in, canvas, cid, relpos, radius, activation)
            self.palette = {
                "big": "lightgrey",
                "small": "grey",
                "outline": "darkgrey",
            }

        def nudge_amount(self):
            return (
                (self.activation[0] / 100) * self.radius[0],
                (self.activation[1] / 100) * self.radius[0],
            )

        def corner_coords(self, type):
            if type == "big":
                x0 = self.rel2abspos()[0] - self.radius[1]
                x1 = self.rel2abspos()[0] + self.radius[1]
                y0 = self.rel2abspos()[1] - self.radius[1]
                y1 = self.rel2abspos()[1] + self.radius[1]
                return (x0, y0, x1, y1)
            elif type == "small":
                x0 = self.rel2abspos()[0] - self.radius[0]
                x1 = self.rel2abspos()[0] + self.radius[0]
                y0 = self.rel2abspos()[1] - self.radius[0]
                y1 = self.rel2abspos()[1] + self.radius[0]
                return (x0, y0, x1, y1)


        def joystick_coords(self):
            cc = self.corner_coords("small")

            x0 = cc[0] + self.nudge_amount()[0]
            x1 = cc[2] + self.nudge_amount()[0]
            y0 = cc[1] + self.nudge_amount()[1]
            y1 = cc[3] + self.nudge_amount()[1]
            return (x0, y0, x1, y1)

        def create(self):
            bcc = self.corner_coords("big")
            scc = self.joystick_coords()
            print(bcc, scc)

            b = self.canvas.create_oval(bcc[0], bcc[1], bcc[2], bcc[3], fill=self.palette["big"], width=0)
            s = self.canvas.create_oval(scc[0], scc[1], scc[2], scc[3], fill=self.palette["small"], width=2, outline=self.palette["outline"])
            self.canvas_id = (s, b)

        def shift(self):
            bcc = self.corner_coords("big")
            scc = self.joystick_coords()
            self.canvas.coords(self.canvas_id[0], scc[0], scc[1], scc[2], scc[3])
            self.canvas.coords(self.canvas_id[1], bcc[0], bcc[1], bcc[2], bcc[3])

        def edit(self, val):
            if self.activation != val:
                self.activation = val
                scc = self.joystick_coords()
                self.canvas.coords(self.canvas_id[0], scc[0], scc[1], scc[2], scc[3])


    def __init__(self, parent, q, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent: Tk = parent
        self.parent.update()
        self.parent.update_idletasks()

        self.q: queue.Queue = q
        self.c: Canvas = Canvas(self, bg="white", width=500, height=500)

        self.test = self.Joystick(self, self.c, ("0", "1"), (0.5, 0.5), (20, 30), (0, 0))
        self.test.create()
        self.test.edit((100,-100))



        self.c.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        self.c.configure(bg="white", width=1000, height=1000)
        self.bind("<Configure>", self.shift)

    def shift(self, event):
        for control in self.ABXY.ctrls:
            control.shift()






            


    



if __name__ == "__main__":   
    root = Tk()
    root.title("XBox Viewer")
    root.geometry("500x500")


    q = queue.Queue(10)
    viewer = XboxViewer(root, q, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)


    root.mainloop()






    


    


