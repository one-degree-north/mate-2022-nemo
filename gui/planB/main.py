"""
A Rhyme to keep in Mind

In case Plan A fails,
And scrutinizing the code is of no avail,

Then stay calm and run main.py twice,
And everything will or might turn out nice!
"""


import tkinter as tk
from PIL import Image, ImageTk


import cv2
import math


class CameraFeed(tk.Label):
    def __init__(self, parent, camera_num):
        tk.Label.__init__(self)
        self.parent = parent
        self.camera_num = camera_num
        self.pack()
        self.capture = cv2.VideoCapture(self.camera_num)
        self.start_camera()

    def start_camera(self):
        # Get single frame from self.capture
        cv2image = cv2.cvtColor(self.capture.read()[1], cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(cv2image)
        
        # Resize image to fit window
        self.dimensions = self.image.size
        resize_dimensions = self.get_resize_dimensions()
        self.image_copy = self.image.resize(resize_dimensions)

        self.imagetk = ImageTk.PhotoImage(self.image_copy)

        self.configure(image=self.imagetk)
        self.after(10, self.start_camera)

    def get_resize_dimensions(self):
        """
        Scales camera feed to fit within window
        """
        bounds = (
            self.parent.winfo_width(),
            math.floor(self.parent.winfo_height() / 1)
        )

        bound_width = bounds[0]
        bound_height = bounds[1]

        base_width = self.dimensions[0]
        base_height = self.dimensions[1]

        width_scale_factor = bound_width / base_width
        height_scale_factor = bound_height / base_height

        limiting_factor = min(width_scale_factor, height_scale_factor)

        new_size = (
            math.floor(limiting_factor * base_width),
            math.floor(limiting_factor * base_height),
        )

        return new_size


if __name__ == "__main__":
    num = int(input("Camera number : "))
    root = tk.Tk()
    root.geometry("1000x500")
    root.update()

    camfeed = CameraFeed(root, num)

    root.mainloop()
