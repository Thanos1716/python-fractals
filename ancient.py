import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class Mandelbrot:
    def __init__(self, coords):
        self.height = int(coords[0])
        self.width = self.height
        self.scale = float(coords[1])
        self.x_off = float(coords[2])
        self.y_off = float(coords[3])

    def update_image(self, resolution: int(50)):
        self.height = resolution
        self.width = resolution
        arr = np.zeros([self.height, self.width], dtype=np.uint8)

        for y in range(self.height):
            for x in range(self.width):
                try:
                    arr[y, x] = self.get_esc(x, y)
                except OverflowError:
                    arr[y, x] = 0
            if y % 30 == 0:
                pass
                # print(y, end=", ")
            if y % 900 == 0:
                print()

        img = Image.fromarray(arr, 'L')
        img.save('mandelbrot.png')

    def get_esc(self, x, y):
        z = 0
        c = complex((self.scale * x) / self.height + self.x_off - self.scale / 2,
                    (self.scale * y) / self.width + self.y_off - self.scale / 2)
        for i in range(100):
            try:
                z = z ** 2 + c
            except OverflowError:
                break
        try:
            dist = np.sqrt(z.real ** 2 + z.imag ** 2)
        except OverflowError:
            dist = 255
            # print("over")
        if np.isnan(dist):
            dist = 255
            # print("nan")
        if np.isinf(dist):
            dist = 255
            # print("inf")
        if dist < 255:
            return dist
        else:
            return dist


class Window:
    def __init__(self, coords):
        self.mandelbrot = Mandelbrot(coords)
        self.window = tk.Tk()
        self.window.title("Explorer")

        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack()
        self.image = ImageTk.PhotoImage(Image.open("mandelbrot.png").resize((600, 600)))
        self.image_id = self.canvas.create_image(20, 20, anchor=tk.NW, image=self.image)

        self.buttons = tk.Frame(master=self.window)
        self.buttons.pack(side=tk.LEFT)

        self.scale_buttons = tk.Frame(master=self.buttons, borderwidth=3, bg="black")
        self.scale_buttons.grid(row=0, column=0)
        self.scale_up = tk.Button(text=" ▲ ", master=self.scale_buttons, command=self.upscale)
        self.scale_up.grid(row=0, column=0)
        self.scale_down = tk.Button(text=" ▼ ", master=self.scale_buttons, command=self.downscale)
        self.scale_down.grid(row=1, column=0)
        self.scale_label = tk.Label(text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
        self.scale_label.grid(row=0, column=1)
        self.scale_size = tk.Entry(width=3, master=self.scale_buttons)
        self.scale_size.grid(row=1, column=1)

        self.resolution = tk.Frame(master=self.buttons)
        self.resolution.grid(row=0, column=1)
        self.resolution_label = tk.Label(text=f"Res: {str(self.mandelbrot.height)}", master=self.resolution)
        self.resolution_label.grid(row=0, column=0)
        self.resolution_size = tk.Entry(width=3, master=self.resolution)
        self.resolution_size.grid(row=0, column=1)
        self.resolution_update = tk.Button(text="Update", master=self.resolution, command=self.update_img)
        self.resolution_update.grid(row=1, column=0)

        self.update_img(True)

        self.offset = tk.Frame(master=self.buttons, bd=3, bg="black")
        self.offset.grid(row=0, column=2)

        self.move_up = tk.Button(text=" ▲ ", master=self.offset, command=self.up)
        self.move_up.grid(row=0, column=0)
        self.move_down = tk.Button(text=" ▼ ", master=self.offset, command=self.down)
        self.move_down.grid(row=0, column=1)

        self.update_pos_labels(True, True)

        self.move_left = tk.Button(text=" ◀ ", master=self.offset, command=self.left)
        self.move_left.grid(row=1, column=0)
        self.move_right = tk.Button(text=" ▶ ", master=self.offset, command=self.right)
        self.move_right.grid(row=1, column=1)

        self.y_dist = tk.Entry(width=3, master=self.offset)
        self.y_dist.grid(row=0, column=3)
        self.x_dist = tk.Entry(width=3, master=self.offset)
        self.x_dist.grid(row=1, column=3)

        self.coordinates = tk.Frame(master=self.buttons)
        self.coordinates.grid(row=0, column=3)
        self.coordinate_buttons = tk.Frame(master=self.coordinates)
        self.coordinate_buttons.grid(row=0, column=0)
        self.export_button = tk.Button(text="Export", command=self.export, master=self.coordinate_buttons)
        self.export_button.grid(row=0, column=1)
        self.goto_button = tk.Button(text="Goto", command=self.goto, master=self.coordinate_buttons)
        self.goto_button.grid(row=0, column=0)
        self.coord_entry = tk.Entry(width=20, master=self.coordinates)
        self.coord_entry.grid(row=0, column=1)

    def update_img(self, update_file: bool = False):
        res = self.mandelbrot.height
        try:
            if int(self.resolution_size.get()) != self.mandelbrot.height:
                res = int(self.resolution_size.get())
                self.resolution_label = tk.Label(text=f"Res: {str(res)}", master=self.resolution)
                self.resolution_label.grid(row=0, column=0)
                update_file = True
        except ValueError:
            pass

        if update_file:
            self.mandelbrot.update_image(res)
        self.image = ImageTk.PhotoImage(Image.open("mandelbrot.png").resize((600, 600)))
        self.canvas.itemconfig(self.image_id, image=self.image)

    def update_pos_labels(self, x: bool = False, y: bool = False):
        if x:
            self.x_label = tk.Label(text=str(self.mandelbrot.x_off)[:5], master=self.offset)
            self.x_label.grid(row=1, column=2)
        if y:
            self.y_label = tk.Label(text=str(self.mandelbrot.y_off)[:5], master=self.offset)
            self.y_label.grid(row=0, column=2)

    def upscale(self):
        try:
            scale_size = float(self.scale_size.get())
        except ValueError:
            scale_size = 1.1
        self.mandelbrot.scale *= scale_size
        self.update_img(True)
        self.scale_label = tk.Label(text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
        self.scale_label.grid(row=0, column=1)

    def downscale(self):
        try:
            scale_size = float(self.scale_size.get())
        except ValueError:
            scale_size = 1.1
        self.mandelbrot.scale /= scale_size
        self.update_img(True)
        self.scale_label = tk.Label(text=f"Scale:\n{str(self.mandelbrot.scale)[:5]}", master=self.scale_buttons)
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

    def goto(self):
        new_coords = self.coord_entry.get().split(", ")
        self.mandelbrot.height, self.mandelbrot.width, self.mandelbrot.scale, self.mandelbrot.x_off, self.mandelbrot.y_off =\
            int(new_coords[0]), int(new_coords[0]), float(new_coords[1]), float(new_coords[2]), float(new_coords[3])
        self.update_img(True)

valid = False
# coords = input("Please enter coordinates:\n").split(", ")
# if coords == ["Full"]:
coords = 50, 3, -0.7, 0

while not valid:
    try:
        for num in coords:
            num = float(num)
        valid = True
    except ValueError:
        coords = input("Invalid coordinates, please try again:\n").split()


win = Window(coords)
win.window.mainloop()
