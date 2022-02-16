import tkinter as tk
from PIL import Image, ImageTk
import cv2
import math


class CameraFeed(tk.Label):
    def __init__(self, parent, camera_no):
        tk.Label.__init__(self, parent)
        self.parent = parent
        self.camera_no = camera_no

        self.frame_interval = 40

        self.cap = cv2.VideoCapture(0)

        self.show_frames()

        self.place(relx=0.5, rely=0.25, anchor=tk.CENTER)


    
    def show_frames(self):
        cv2image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
        
        self.img = Image.fromarray(cv2image)
        self.aspect = self.img.size
        self.img = self.img.resize(
            (self.parent.winfo_width(), self.parent.winfo_height())
        )
        self.img_copy = self.img.resize(self.grd())
        self.imgtk = ImageTk.PhotoImage(self.img_copy)
        self.configure(image=self.imgtk)

        self.after(40, self.show_frames)

    def grd(self):
        # Get resize dimesions

        bounds = (self.parent.winfo_width(), math.floor(self.parent.winfo_height()/2))
        print(bounds)
        
        bound_width = bounds[0]
        bound_height = bounds[1]

        base_width = self.aspect[0]
        base_height = self.aspect[1]

        width_scale_factor = bound_width / base_width
        height_scale_factor = bound_height / base_height

        limiting_factor = min(width_scale_factor, height_scale_factor)

        new_size = (
            math.floor(limiting_factor * base_width),
            math.floor(limiting_factor * base_height)
        )

        return new_size






class SensorReadout(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.update()

        self.configure(bg="green")

        self.place(relx=0.5, rely=0.75, relheight=0.5, relwidth=1, anchor=tk.CENTER)

root = tk.Tk()

root.geometry("600x600")
root.update()

test = CameraFeed(root, 1)
test2 = SensorReadout(root)

root.mainloop()

