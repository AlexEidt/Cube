import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from linalg import Vector, Matrix

WIDTH = 640
HEIGHT = 360
COLOR = (57, 255, 20)
THICKNESS = 4
DISTANCE = 2
CENTER = Vector([WIDTH / 2, HEIGHT / 2])


def main():
    root = tk.Tk()
    root.title("Cube")
    root.resizable(width=False, height=False)

    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    label = tk.Label(root)

    points = []
    for i in range(8):
        s = format(i, "03b")  # Zero-padded binary representation of i.
        points.append(Vector([float(d) - 0.5 for d in s]))

    stop = []
    root.protocol("WM_DELETE_WINDOW", lambda: stop.append(0))

    angle = 0.0
    while not stop:
        draw_cube(points, draw, angle)

        # Update screen.
        ph_image = ImageTk.PhotoImage(image)
        label.configure(image=ph_image)
        label.image = ph_image
        label.pack()

        root.update_idletasks()
        root.update()

        angle += 0.002


def draw_cube(points, image, angle):
    image.rectangle((0, 0, WIDTH, HEIGHT), 0)  # Clear screen.

    cos, sin = math.cos(angle), math.sin(angle)
    rx = Matrix([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
    ry = Matrix([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
    rz = Matrix([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    rotation = rx * ry * rz

    cube = []
    for vector in points:
        rotated = rotation * vector

        z = 1 / (DISTANCE - rotated.z)
        projection = Matrix([[z, 0, 0], [0, z, 0]])
        cube.append((projection * rotated) * (WIDTH / 2) + CENTER)

    for i in range(4):
        image.line((*cube[i], *cube[i + 4]), fill=COLOR, width=THICKNESS)

    for i in range(0, 8, 2):
        image.line((*cube[i], *cube[i + 1]), fill=COLOR, width=THICKNESS)

    for i in range(2):
        image.line((*cube[i], *cube[i + 2]), fill=COLOR, width=THICKNESS)
        image.line((*cube[i + 4], *cube[i + 6]), fill=COLOR, width=THICKNESS)


if __name__ == "__main__":
    main()
