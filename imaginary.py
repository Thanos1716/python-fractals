from tkinter import Tk, Checkbutton, IntVar


class Test:
    def __init__(self):
        self.greyscale = IntVar()


class MyGUI:
    def __init__(self, window):
        self.test = Test()
        self.var = IntVar()
        self.c = Checkbutton(
            window, text="Enable Tab",
            command=lambda: self.toggle(self.test.greyscale))
        self.c.pack()

    def toggle(self, var):
        var.set(not var.get())
        print(var.get())


root = Tk()
gui = MyGUI(root)
root.mainloop()
# from tqdm import tqdm

# for i in tqdm(range(int(9e5))):
#     pass

# list = "Some words".split()
# for i in list:
#     print(i)

# print(list[i] for i in range(len(list)))


"""import tkinter as tk

# --- functions ---

def on_click():
    # change image on canvas
    canvas.itemconfig(image_id, image=image2)

# --- main ---

root = tk.Tk()

# canvas for image
canvas = tk.Canvas(root, width=60, height=60)
canvas.pack()

# button to change image
button = tk.Button(root, text="Change", command=on_click)
button.pack()

# images
image1 = tk.PhotoImage(file="ball1.gif")
image2 = tk.PhotoImage(file="ball2.gif")

# set first image on canvas
image_id = canvas.create_image(0, 0, anchor='nw', image=image1)

root.mainloop()

from tkinter import *
from PIL import ImageTk, Image
root = Tk()
canvas = Canvas(root, width=300, height=300)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("mandelbrot.png"))
canvas.create_image(20, 20, anchor=NW, image=img)
root.mainloop()

import tkinter as tk

window = tk.Tk()

for i in range(3):
    for j in range(3):
        frame = tk.Frame(
            master=window,
            relief=tk.FLAT,
            borderwidth=4
        )

        frame.grid(row=i, column=j)
        label = tk.Button(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()

window.mainloop()

import math
import cmath
import numpy as np
from PIL import Image

height = 250
width = 250
arr = np.zeros([width, height], dtype=np.uint8)


def get_esc(x, y):
    z = 0
    c = complex((2*y)/height-1, (2*x)/width-1)
    for i in range(100):
        try:
            z = z**2 + c
        except OverflowError:
            break

    try:
        if math.sqrt(z.real**2 + z.imag**2) < 255:
            return math.sqrt(z.real**2 + z.imag**2)
        else:
            return 255
    except OverflowError:
        return 255


for y in range(height):
    for x in range(width):
        arr[x, y] = get_esc(x, y)


img = Image.fromarray(arr, 'L')
img.save('mandelbrot.png')
img.show()



# import math
# import cmath
# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image
# # Initializing real numbers
# height = 255
# width = 255
# max_iterations = 10
# arr = np.zeros([width, height], dtype=np.uint8)
#
# for y in range(height):
#     for x in range(width):
#         z = 0
#         c = complex((2*x-1)/width, (2*y-1)/height)
#         for i in range(max_iterations):
#             try:
#                 z = z**2 + c
#             except OverflowError:
#                 break
#         try:
#             arr[x, y] = math.sqrt(z.real**2 + z.imag**2) % 255
#         except:
#             arr[x, y] = 0
#
#         if abs((2*x-1)/width) == 1 and abs((2*y-1)/height) == 1:
#             arr[(2*x-1)/width, (2*y-1)/height] = 255
#         # print(z.conjugate())
#         # print(z)
#
# img = Image.fromarray(arr, 'L')
# img.save('mandelbrot.png')
# img.show()
#
# for i in range(0):
#     z = z**2+c
#     print(z)
#
#
# # arr[:, :, 3] = 255
"""
