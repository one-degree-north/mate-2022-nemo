
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread

import cv2
import math


class CameraBox(tk.Label):
    def __init__(self, parent, relx, rely):
        tk.Label.__init__(self)
        self.parent = parent
        self.relx = relx
        self.rely = rely


        self.start_camera()

        self.place(relx=relx, rely=rely, relheight=0.5, relwidth=0.5, anchor=tk.CENTER)

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)

        cv2image = cv2.cvtColor(self.capture.read()[1], cv2.COLOR_BGR2RGB)
        
        self.image = Image.fromarray(cv2image)
        self.dimensions = self.image.size

        resize_dimensions = self.get_resize_dimensions()

        self.image_copy = self.image.resize(resize_dimensions)
        
        self.imagetk = ImageTk.PhotoImage(self.image_copy)
        
        self.configure(image=self.imagetk)
        self.after(10, self.start_camera)

    def get_resize_dimensions(self):
        bounds = (self.parent.winfo_width(), math.floor(self.parent.winfo_height()/2))
        print("this")
        print(bounds)
        print("that")
        
        bound_width = bounds[0]
        bound_height = bounds[1]

        base_width = self.dimensions[0]
        base_height = self.dimensions[1]

        width_scale_factor = bound_width / base_width
        height_scale_factor = bound_height / base_height

        limiting_factor = min(width_scale_factor, height_scale_factor)

        new_size = (
            math.floor(limiting_factor * base_width),
            math.floor(limiting_factor * base_height)
        )

        return new_size

class CameraFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent



        self.configure(
            width=self.parent.winfo_width(),
            height=self.parent.winfo_height(),
            bg="green"
        )

        self.update()
        self.start_cameras()

        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)

        print(self.winfo_width(), self.winfo_height())


    def start_cameras(self):
        self.camera1 = CameraBox(self, relx=0.5, rely=0.25)
        self.camera2 = CameraBox(self, relx=0.5, rely=0.75)




if __name__ == "__main__":
    def run():
        root = tk.Tk()
        root.geometry("1000x500")
        root.update()

    main = Thread(target=run)


    test_thread = Thread(target=lambda: CameraBox(root, 0.25, 0.25))
    test2_thread = Thread(target=lambda: CameraBox(root, 0.75, 0.25))
    
    test_thread.start()
    test2_thread.start()

    test_thread.join()
    test2_thread.join()
    
    # test = CameraBox(root, 0.25, 0.25)
    # test2 = CameraBox(root, 0.75, 0.25)



    root.mainloop()
