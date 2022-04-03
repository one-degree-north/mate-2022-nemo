from dataclasses import dataclass
from tkinter import Canvas, Frame, CENTER, Tk

import queue
from typing import Union
from time import sleep
from math import floor

@dataclass
class Display:
    activation: float
    pos: tuple[float, float]
    radius: Union[int, tuple[int, int]] # smaller then bigger radius for the float
    control_type: str

colors = {
    "a": {"off": "#008000", "on": "#6fc76f"},
    "b": {"off": "#8f0707", "on": "#b56b6b"},
    "x": {"off": "#162c7a", "on": "#6775a6"},
    "y": {"off": "#999100", "on": "#ccc881"},
}

real_control_name = {
    "6": "a",
    "7": "b",
}




class XboxViewer(Frame):

    def __init__(self, parent, q, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent: Tk = parent
        self.parent.update()

        self.q: queue.Queue = q

        self.c: Canvas = Canvas(self, bg="white", width=500, height=500)
        self.h, self.w = 500,500


        self.c.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        self.c.configure(width=1000, height=1000)
        # self.c.bind("<Configure>", self.move)
        self.bind("<Configure>", self.move)

        self.controls = {
            "6": Display(0, (0.5, 0.5), 15, "abxy_button"),
            "7": Display(0, (0.5, 0.75), 15, "abxy_button"),

            "0": Display(0, (0.25, 0.25), (30, 45), "joystick"),
            "1": Display(0, (0.25, 0.25), (30, 45), "joystick")
        }
        self.colors = {
            "a": {"off": "#008000", "on": "#6fc76f"},
            "b": {"off": "#8f0707", "on": "#b56b6b"},
            "x": {"off": "#162c7a", "on": "#6775a6"},
            "y": {"off": "#999100", "on": "#ccc881"},
        }
        self.real_control_name = {
            "6": "a",
            "7": "b",
        }

        self.abxy_buttons_canvas_item_ids = {}
        self.joystick_canvas_item_ids = {}

        self.associated_pairs = {
            "0": "1",
            "1": "0"
        }

        for cid in self.controls.keys():
            self.create_control(cid)


    def check_queue(self):

        if self.q.qsize() == 2:
            cid = self.q.get()
            value = self.q.get()

            self.edit_control(cid, value)


        instructions = ""
        if self.q.qsize() == 0:
            instructions = input("cid: ")
        elif self.q.qsize() == 1:
            instructions = int(input("val: "))

        self.q.put(instructions)

        self.after(2, self.check_queue)

    def create_control(self, cid):
        if cid == "1":
            return 
        if self.controls[cid].control_type == "abxy_button":
            print("Creating an abxy button")
            pos = self.rel2abspos(cid)
            print(pos)

            radius = self.controls[cid].radius
            x0 = pos[0] - radius
            y0 = pos[1] - radius
            x1 = pos[0] + radius
            y1 = pos[1] + radius

            _color = ""

            if self.controls[cid].activation == 0:
                rcn = real_control_name[cid]
                _color = colors[rcn]["off"]
            elif self.controls[cid].activation == 1:
                rcn = real_control_name[cid]
                _color = colors[rcn]["off"]

            # print(_color)


            _id: int = self.c.create_oval(x0, y0, x1, y1, fill=_color, width=2, outline=_color)
            self.abxy_buttons_canvas_item_ids[cid] = _id

        elif self.controls[cid].control_type == "joystick":
            print("Creating a joystick")
            pos = self.rel2abspos(cid)
            print(pos)

            big_radius = self.controls[cid].radius[1]
            x0 = pos[0] - big_radius
            y0 = pos[1] - big_radius
            x1 = pos[0] + big_radius
            y1 = pos[1] + big_radius
            print(x0, x1)

            _id: int = self.c.create_oval(x0, y0, x1, y1, fill="lightgrey", width=0)
            print(f"Big circle created with {_id = }")
            self.joystick_canvas_item_ids[cid + "+"] = _id



            small_radius = self.controls[cid].radius[0]
            x0 = pos[0] - small_radius
            y0 = pos[1] - small_radius
            x1 = pos[0] + small_radius
            y1 = pos[1] + small_radius

            _id: int = self.c.create_oval(x0, y0, x1, y1, fill="darkgrey", width=2, outline="grey")
            print(f"Small circle created with {_id = }")
            self.joystick_canvas_item_ids[cid + "-"] = _id





    def edit_control(self, cid, val):
        if cid not in self.controls.keys():
            # print("cid not drawn to display yet")
            return

        if self.controls[cid].activation != val:
            self.controls[cid].activation = val

            if self.controls[cid].control_type == "abxy_button":
                if val == 1:
                    rcn = real_control_name[cid]
                    _color = colors[rcn]["on"]
                    outline = colors[rcn]["off"]
                    self.c.itemconfig(self.abxy_buttons_canvas_item_ids[cid], fill=_color, outline=outline, width=2)
                elif val == 0:
                    rcn = real_control_name[cid]
                    _color = colors[rcn]["off"]
                    self.c.itemconfig(self.abxy_buttons_canvas_item_ids[cid], fill=_color, width=2)

            if self.controls[cid].control_type == "joystick":
                self.shift_joystick(cid)

    def joystick_pixel_shift_amount(self, cid):
        # print(f"Acivation of {cid} = {self.controls[cid].activation}")
        return (self.controls[cid].activation / 100) * self.controls[cid].radius[0]

    def shift_joystick(self, cid):
        pos = self.rel2abspos(cid)
        cc = self.corner_coords(pos, self.controls[cid].radius[0])

        dx, dy = 0,0
        if cid == "0":
            dx = self.joystick_pixel_shift_amount(cid)
            dy = self.joystick_pixel_shift_amount(self.associated_pairs[cid])

        elif cid == "1":
            dx = self.joystick_pixel_shift_amount(self.associated_pairs[cid])
            dy = self.joystick_pixel_shift_amount(cid)


        x0, x1 = cc[0] + dx, cc[2] + dx
        y0, y1 = cc[1] - dy, cc[3] - dy

        if cid == "1":
            cid = "0"
        _id = self.joystick_canvas_item_ids[cid + "-"]
        self.c.coords(_id, x0, y0, x1, y1)

    def move(self, event):
        def clean_id(cid) -> str:
            # print(f"Converted {cid = } to", end=" ")
            if cid.endswith("+"):
                # print(cid.replace("+", ""))
                return cid.replace("+", "")
            elif cid.endswith("-"):
                # print(cid.replace("-", ""))
                return cid.replace("-", "")
        
        self.w = self.winfo_width()
        self.h = self.winfo_height()
        # print(self.w, self.h)

        self.c.configure(width=self.w, height=self.h)

        # shifting the controls

        for cid, _id in self.abxy_buttons_canvas_item_ids.items():
            pos = self.rel2abspos(cid)
            radius = self.controls[cid].radius
            cc = self.corner_coords(pos, radius)
            x0, y0, x1, y1 = cc[0], cc[1], cc[2], cc[3]
            self.c.coords(_id, x0, y0, x1, y1)

        cids_completed = []
        # print("Joystick items below: ")
        # print(self.joystick_canvas_item_ids)
        for cid in self.joystick_canvas_item_ids.keys():
            ccid = clean_id(cid)
            if ccid in cids_completed: # If a button has already been redrawn, skip to 
                continue


            pos = self.rel2abspos(ccid)
            
            big_radius = self.controls[ccid].radius[1]
            cc = self.corner_coords(pos, big_radius)
            x0, y0, x1, y1 = cc[0], cc[1], cc[2], cc[3]
            _id = self.joystick_canvas_item_ids[ccid + "+"]
            self.c.coords(_id, x0, y0, x1, y1)

            small_radius = self.controls[ccid].radius[0]
            cc = self.corner_coords(pos, small_radius)
            x0, y0, x1, y1 = cc[0], cc[1], cc[2], cc[3]
            _id = self.joystick_canvas_item_ids[ccid + "-"]
            self.c.coords(_id, x0, y0, x1, y1)

            cids_completed.append(ccid)

        for cid in self.joystick_canvas_item_ids.keys():
            cid = self.clean_id(cid)
            self.shift_joystick(cid)



            
            
    def corner_coords(self, pos, r):
        return (pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r)
            


    def rel2abspos(self, cid):
        x = self.w * self.controls[cid].pos[0]
        y = self.h * self.controls[cid].pos[1]
        # print("abspos: ", x, y)

        return (x, y)

    def clean_id(self, cid) -> str:
        # print(f"Converted {cid = } to", end=" ")
        if cid.endswith("+"):
            # print(cid.replace("+", ""))
            return cid.replace("+", "")
        elif cid.endswith("-"):
            # print(cid.replace("-", ""))
            return cid.replace("-", "")
    



if __name__ == "__main__":   
    root = Tk()
    root.geometry("500x500")
    root.update()
    root.update_idletasks()



    q = queue.Queue(10)
    viewer = XboxViewer(root, q, bg="white", width=500, height=500)
    viewer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
    viewer.check_queue()

    root.mainloop()






    


    


