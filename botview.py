from dataclasses import dataclass
from tkinter import Canvas, Frame, CENTER, Tk

import queue
from typing import Union
from time import sleep
from math import floor, sin, cos





class XboxViewer(Frame):

    class Control(object):
        ctrls = []
        
        def __init__(self, frame_in, canvas, element_no, relpos, radius, activation=0):
            self.frame_in: Frame = frame_in
            self.canvas: Canvas = canvas
            self.element_no = element_no
            self.relpos = relpos
            self.radius = radius
            self.activation = activation

            self.palette = {}

            self.ctrls.append(self)

        def create(self):
            cc = self.corner_coords()
            self.canvas_id = self.canvas.create_oval(cc[0], cc[1], cc[2], cc[3], width=2, fill=self.dip_paintbrush(), outline=self.palette[self.element_no]["off"]) 

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

    class Joystick(Control):
        def __init__(self, frame_in, canvas, element_no, relpos, radius, activation: tuple):
            """
            element_no and radius are tuples
            main in front
            """
            super().__init__(frame_in, canvas, element_no, relpos, radius, activation)
            self.palette = {
                "big": "lightgrey",
                "small": "grey",
                "outline": "darkgrey",
            }

        def nudge_amount(self):
            return (
                (self.activation[0]) * self.radius[0],
                (-self.activation[1]) * self.radius[0],
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

            self.big = self.canvas.create_oval(bcc[0], bcc[1], bcc[2], bcc[3], fill=self.palette["big"], width=0)
            self.small = self.canvas.create_oval(scc[0], scc[1], scc[2], scc[3], fill=self.palette["small"], width=3, outline=self.palette["outline"])

        def shift(self):
            bcc = self.corner_coords("big")
            scc = self.joystick_coords()
            self.canvas.coords(self.small, scc[0], scc[1], scc[2], scc[3])
            self.canvas.coords(self.big, bcc[0], bcc[1], bcc[2], bcc[3])

        def edit(self, val):
            if self.activation != val:
                self.activation = val
                scc = self.joystick_coords()
                self.canvas.coords(self.small, scc[0], scc[1], scc[2], scc[3])

    class Trigger(Control):
        def __init__(self, frame_in, canvas, element_no, relpos, radius, activation):
            """
            In this case, radius[0] is the width, radius[1] is the height
            """
            super().__init__(frame_in, canvas, element_no, relpos, radius, activation)
            self.palette = {
                "bar": "#9c9c9c",
                "fill": "#32a852"
            }

        def create(self):
            bar_cc = self.corner_coords()
            fill_cc = self.fill_coords()
            print(bar_cc, fill_cc)
            
            bar = self.canvas.create_rectangle(bar_cc[0], bar_cc[1], bar_cc[2], bar_cc[3], fill=self.palette["bar"], width=0)
            fill = self.canvas.create_rectangle(fill_cc[0], fill_cc[1], fill_cc[2], fill_cc[3], fill=self.palette["fill"], width=0)

            self.canvas_id = (fill, bar)

        def shift(self):
            bar_cc = self.corner_coords()
            fill_cc = self.fill_coords()

            self.canvas.coords(self.canvas_id[1], bar_cc[0], bar_cc[1], bar_cc[2], bar_cc[3])
            self.canvas.coords(self.canvas_id[0], fill_cc[0], fill_cc[1], fill_cc[2], fill_cc[3])

        def edit(self, val):
            if self.activation != val:
                self.activation = val

                bar_cc = self.corner_coords()
                fill_cc = self.fill_coords()

                self.canvas.coords(self.canvas_id[1], bar_cc[0], bar_cc[1], bar_cc[2], bar_cc[3])
                self.canvas.coords(self.canvas_id[0], fill_cc[0], fill_cc[1], fill_cc[2], fill_cc[3])

        def corner_coords(self):
            x0 = self.rel2abspos()[0] - self.radius[0]
            x1 = self.rel2abspos()[0] + self.radius[0]
            y0 = self.rel2abspos()[1] - self.radius[1]
            y1 = self.rel2abspos()[1] + self.radius[1]
            return (x0, y0, x1, y1)

        def fill_amount(self):
            return 2 * self.radius[0] - self.activation / 100 * self.radius[0] * 2

        def fill_coords(self):
            cc = self.corner_coords()
            amount = self.fill_amount()
            # print(amount)
            x0 = cc[0]
            x1 = cc[2] - amount
            y0 = cc[1]
            y1 = cc[3]
            return (x0, y0, x1, y1)



    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent: Tk = parent
        self.parent.update()
        self.parent.update_idletasks()


        self.c: Canvas = Canvas(self, bg="white", width=500, height=500)

        self.test3 = self.Joystick(self, self.c, 1, (0.5, 0.5), (75, 100), (0, 0))
        self.test3.create()

        # self.after(10000, self.test4.edit, 0)
        # self.after(10000, self.test5.edit, 0)




        self.c.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        self.c.configure(bg="white", width=1000, height=1000)
        self.bind("<Configure>", self.shift)

    def shift(self, event):
        for control in self.Control.ctrls:
            control.shift()





def create_view():
    root = Tk()
    root.title("XBox Viewer")
    root.geometry("500x500")


    viewer = XboxViewer(root, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

    # def checker():
    #     print(q.get())
    #     root.after(20, checker)

    # checker()

    root.mainloop()


            


    



if __name__ == "__main__":   
    create_view()






    


    


