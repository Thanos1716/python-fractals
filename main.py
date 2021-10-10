import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import time
from tqdm import tqdm
import os
import concurrent.futures
import random

save_resolution = 512

# Rendering a 1000px x 1000px Mandelbrot set
# Finished rendering in 5 minutes, 29 seconds originally
# Finished rendering in 5 minutes, 46 seconds with threading
# Finished rendering in 6 minutes, 35 seconds with multiprocessing


class Gradient:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.diff = [start[i] - end[i] for i in range(len(start))]

    def get_gradient(self, pos):
        return [self.end[j] + self.diff[j] * pos for j in range(len(self.diff))]


class Mandelbrot:
    def __init__(self, coords):
        self.height = int(coords[0])
        self.width = self.height
        self.scale = float(coords[1])
        self.x_off = float(coords[2])
        self.y_off = float(coords[3])
        self.gradient = Gradient(
            *[[random.randint(0, 255) for _ in range(3)] for _ in range(2)])
        self.iterations = 255
        self.greyscale = True

    def update_image(self, resolution: int(50)):
        self.height = resolution
        self.width = resolution
        if self.greyscale:
            arr = np.zeros([self.height, self.width], dtype=np.uint8)
        else:
            arr = np.zeros([self.height, self.width, 3], dtype=np.uint8)

        start = time.time()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.update_column, [
                                   y for y in range(self.height)])

            for y, result in zip(range(self.height), results):
                arr[y] = result
            if self.height >= save_resolution and y == 0:
                elapsed = time.time() - start
                print(
                    f"Estimated completion time is {round((elapsed * self.height) / 60)} minutes, {round(elapsed * self.height) % 60} seconds")
                print("Seed: {}".format(", ".join(str(i)
                                                  for i in [self.height, self.scale, self.x_off, self.y_off])))

            elapsed = time.time() - start
            print(f"{round(elapsed / 60)}:{str(elapsed % 60)[:4]}")

        if self.greyscale:
            img = Image.fromarray(arr, 'L')
        else:
            img = Image.fromarray(arr, 'RGB')

        img.save('mandelbrot.png')

        if self.height >= save_resolution:
            if not os.path.exists("saves"):
                os.mkdir("saves")
            img.save("saves/{}.png".format(", ".join(str(i)
                                                     for i in [self.height, self.scale, self.x_off, self.y_off])))

    def update_column(self, y):
        column = []
        for x in range(self.width):
            try:
                column.append(self.get_escape_to_inf(x, y))
            except OverflowError:
                if self.greyscale:
                    column.append(127)
                else:
                    column.append([255, 0, 0])

        return column

    def get_escape_to_inf(self, x, y):
        z = 0
        c = complex((self.scale * x) / self.height + self.x_off - self.scale / 2,
                    (self.scale * y) / self.width + self.y_off - self.scale / 2)
        # c = complex(-0.84, -0.17)
        for i in range(self.iterations):
            try:
                n = z ** 2 + c
                if np.isnan(n):  # For imaginary numbers that escape to infinity
                    break
                else:
                    z = n
            except OverflowError:  # For real numbers that escape to infinity
                break
        if i == self.iterations - 1:
            if self.greyscale:
                return 0
            else:
                return [0, 0, 0]

        elif self.greyscale:
            return int(255 * (i / self.iterations))
        else:
            return [int(self.gradient.get_gradient(i / self.iterations)[n]) for n in range(3)]


class Window:
    def __init__(self, coords):
        self.window = tk.Tk()
        self.window.title("Mandelbrot Explorer")

        self.mandelbrot = Mandelbrot(coords)
        self.mandelbrot.update_image(50)

        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack()
        self.image = ImageTk.PhotoImage(
            Image.open("mandelbrot.png").resize((600, 600)))
        self.image_id = self.canvas.create_image(
            20, 20, anchor=tk.NW, image=self.image)

        self.buttons = tk.Frame(master=self.window)
        self.buttons.pack(side=tk.LEFT)

        self.scale_buttons = tk.Frame(
            master=self.buttons, borderwidth=3, bg="black")
        self.scale_buttons.grid(row=0, column=0)
        self.scale_up = tk.Button(
            text=" ▲ ", master=self.scale_buttons, command=self.upscale)
        self.scale_up.grid(row=0, column=0)
        self.scale_down = tk.Button(
            text=" ▼ ", master=self.scale_buttons, command=self.downscale)
        self.scale_down.grid(row=1, column=0)
        self.scale_label = tk.Label(
            text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
        self.scale_label.grid(row=0, column=1)
        self.scale_size = tk.Entry(width=3, master=self.scale_buttons)
        self.scale_size.grid(row=1, column=1)

        self.resolution = tk.Frame(master=self.buttons)
        self.resolution.grid(row=0, column=1)
        self.resolution_label = tk.Label(
            text=f"Res: {str(self.mandelbrot.height)}", master=self.resolution)
        self.resolution_label.grid(row=0, column=0)
        self.resolution_size = tk.Entry(width=3, master=self.resolution)
        self.resolution_size.grid(row=0, column=1)
        self.resolution_update = tk.Button(
            text="Update", master=self.resolution, command=self.update_img)
        self.resolution_update.grid(row=1, column=0)

        self.greyscale_box = tk.Checkbutton(
            master=self.resolution, text="B&W", command=lambda: self.toggle(self.mandelbrot.greyscale))
        self.greyscale_box.select()
        self.greyscale_box.grid(row=1, column=1)

        self.update_img(True)

        self.offset = tk.Frame(master=self.buttons, bd=3, bg="black")
        self.offset.grid(row=0, column=2)

        self.move_up = tk.Button(
            text=" ▲ ", master=self.offset, command=self.up)
        self.move_up.grid(row=0, column=0)
        self.move_down = tk.Button(
            text=" ▼ ", master=self.offset, command=self.down)
        self.move_down.grid(row=0, column=1)

        self.update_pos_labels(True, True)

        self.move_left = tk.Button(
            text=" ◀ ", master=self.offset, command=self.left)
        self.move_left.grid(row=1, column=0)
        self.move_right = tk.Button(
            text=" ▶ ", master=self.offset, command=self.right)
        self.move_right.grid(row=1, column=1)

        self.y_dist = tk.Entry(width=3, master=self.offset)
        self.y_dist.grid(row=0, column=3)
        self.x_dist = tk.Entry(width=3, master=self.offset)
        self.x_dist.grid(row=1, column=3)

        self.coordinates = tk.Frame(master=self.buttons)
        self.coordinates.grid(row=0, column=3)
        self.coordinate_buttons = tk.Frame(master=self.coordinates)
        self.coordinate_buttons.grid(row=0, column=0)
        self.export_button = tk.Button(
            text="Export", command=self.export, master=self.coordinate_buttons)
        self.export_button.grid(row=0, column=1)
        self.goto_button = tk.Button(
            text="Goto", command=self.goto, master=self.coordinate_buttons)
        self.goto_button.grid(row=0, column=0)
        self.coord_entry = tk.Entry(width=20, master=self.coordinates)
        self.coord_entry.grid(row=0, column=1)

    def update_img(self, update_file: bool = False):
        res = self.mandelbrot.height
        try:
            if int(self.resolution_size.get()) != self.mandelbrot.height:
                res = int(self.resolution_size.get())
                self.resolution_label = tk.Label(
                    text=f"Res: {str(res)}", master=self.resolution)
                self.resolution_label.grid(row=0, column=0)
                update_file = True
        except ValueError:
            pass

        if update_file:
            self.mandelbrot.update_image(res)
        self.image = ImageTk.PhotoImage(
            Image.open("mandelbrot.png").resize((600, 600)))
        self.canvas.itemconfig(self.image_id, image=self.image)

    def update_pos_labels(self, x: bool = False, y: bool = False):
        if x:
            self.x_label = tk.Label(text=str(self.mandelbrot.x_off)[
                                    :5], master=self.offset)
            self.x_label.grid(row=1, column=2)
        if y:
            self.y_label = tk.Label(text=str(self.mandelbrot.y_off)[
                                    :5], master=self.offset)
            self.y_label.grid(row=0, column=2)

    def upscale(self):
        try:
            scale_size = float(self.scale_size.get())
        except ValueError:
            scale_size = 1.1
        self.mandelbrot.scale *= scale_size
        self.update_img(True)
        self.scale_label = tk.Label(
            text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
        self.scale_label.grid(row=0, column=1)

    def downscale(self):
        try:
            scale_size = float(self.scale_size.get())
        except ValueError:
            scale_size = 1.1
        self.mandelbrot.scale /= scale_size
        self.update_img(True)
        self.scale_label = tk.Label(
            text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
        self.scale_label.grid(row=0, column=1)

    def up(self):
        try:
            offset = float(self.y_dist.get()) * self.mandelbrot.scale
        except ValueError:
            offset = 0.2 * self.mandelbrot.scale
        self.mandelbrot.y_off -= offset
        self.update_img(True)
        self.update_pos_labels(False, True)

    def down(self):
        try:
            offset = float(self.y_dist.get()) * self.mandelbrot.scale
        except ValueError:
            offset = 0.2 * self.mandelbrot.scale
        self.mandelbrot.y_off += offset
        self.update_img(True)
        self.update_pos_labels(False, True)

    def right(self):
        try:
            offset = float(self.x_dist.get()) * self.mandelbrot.scale
        except ValueError:
            offset = 0.2 * self.mandelbrot.scale
        self.mandelbrot.x_off += offset
        self.update_img(True)
        self.update_pos_labels(True)

    def left(self):
        try:
            offset = float(self.x_dist.get()) * self.mandelbrot.scale
        except ValueError:
            offset = 0.2 * self.mandelbrot.scale
        self.mandelbrot.x_off -= offset
        self.update_img(True)
        self.update_pos_labels(True)

    def export(self):
        self.coord_entry.delete(0, tk.END)
        self.coord_entry.insert(0, ", ".join(
            [str(self.mandelbrot.height), str(self.mandelbrot.scale),
             str(self.mandelbrot.x_off), str(self.mandelbrot.y_off)]))
        print(", ".join(
            [str(self.mandelbrot.height), str(self.mandelbrot.scale),
             str(self.mandelbrot.x_off), str(self.mandelbrot.y_off)]))

    def goto(self):
        new_coords = self.coord_entry.get().split(", ")
        self.mandelbrot.height, self.mandelbrot.width, self.mandelbrot.scale, self.mandelbrot.x_off, self.mandelbrot.y_off = \
            int(new_coords[0]), int(new_coords[0]), float(
                new_coords[1]), float(new_coords[2]), float(new_coords[3])
        self.update_img(True)

    def toggle(self, var):
        self.mandelbrot.greyscale = not self.mandelbrot.greyscale


coords = 50, 3, -0.7, 0

win = Window(coords)
win.window.mainloop()
