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
        
        def __init__(self, frame_in, canvas, cid, relpos, w_radius, h_radius, activation=0):
            self.frame_in: Frame = frame_in
            self.canvas: Canvas = canvas
            self.cid = cid
            self.relpos = relpos
            self.w_radius = w_radius
            self.h_radius = h_radius
            self.activation = activation

            self.ctrls.append(self)

        def create(self):
            cc = self.corner_coords()
            print(cc)
            self.ctrl_ids[self.cid] = self.canvas.create_oval(cc[0], cc[1], cc[2], cc[3], width=2, fill=self.dip_paintbrush()) 

        def corner_coords(self):
            x0 = self.rel2abspos()[0] - self.w_radius
            x1 = self.rel2abspos()[0] + self.w_radius
            y0 = self.rel2abspos()[1] - self.h_radius
            y1 = self.rel2abspos()[1] + self.h_radius
            return (x0, y0, x1, x1)

        def rel2abspos(self):
            x = self.frame_in.parent.winfo_width() * self.relpos[0]
            y = self.frame_in.parent.winfo_height() * self.relpos[1]
            return (x, y)

        def dip_paintbrush(self):
            return "white"

        @classmethod
        def fetch_cids(cls):
            return cls.ctrl_ids
        
        @classmethod
        def fetch_all_controls(cls):
            return cls.ctrls

    class ABXY(Control):
        def __init__(self, frame_in, canvas, cid, relpos, w_radius, h_radius, activation):
            super().__init__(frame_in, canvas, cid, relpos, w_radius, h_radius, activation)
            self.palette = {
                "6": {"on": "", "off": ""},
            }

        def dip_paintbrush(self):
            paint = self.palette[self.cid]["on"] if self.activation == 1 else self.palette[self.cid]["off"]
            return paint

    class Joystick(Control):
        def __init__(self, frame_in, canvas, cid: tuple, relpos, w_radius, h_radius, activation: tuple):
            super().__init__(frame_in, canvas, cid, relpos, w_radius, h_radius, activation)
            self.palette = {
                "big": "lightgrey",
                "small": "grey",
                "outline": "darkgrey",
            }

        def nudge_amount(self):
            return (
                (self.activation[0] / 100) * self.w_radius,
                (self.activation[1] / 100) * self.h_radius,
            )

        def joystick_coords(self, cc=None):
            if cc == None:
                cc = self.corner_coords()

            x0 = cc[0] - self.nudge_amount()[0]
            x1 = cc[2] + self.nudge_amount()[0]
            y0 = cc[1] - self.nudge_amount()[1]
            y1 = cc[3] + self.nudge_amount()[1]
            return (x0, y0, x1, y1)

        def create(self):
            bcc = self.corner_coords()
            scc = self.joystick_coords(bcc)

            b = self.canvas.create_oval(bcc[0], bcc[1], bcc[2], bcc[3], fill=self.palette["big"], width=0)
            s = self.canvas.create_oval(scc[0], scc[1], scc[2], scc[3], fill=self.palette["small"], width=2, outline=self.palette["outline"])

            return (s, b)

    def __init__(self, parent, q, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent: Tk = parent
        self.parent.update()
        self.parent.update_idletasks()

        self.q: queue.Queue = q
        self.c: Canvas = Canvas(self, bg="white", width=500, height=500)

        self.test = self.ABXY(self, self.c, "6", (0.5, 0.5), 20, 20, 0)
        self.test.create()

        self.c.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        self.c.configure(bg="purple", width=1000, height=1000)




            


    



if __name__ == "__main__":   
    root = Tk()
    root.title("XBox Viewer")
    root.geometry("500x500")


    q = queue.Queue(10)
    viewer = XboxViewer(root, q, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)


    root.mainloop()






    


    


