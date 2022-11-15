import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from linalg import Vector, Matrix

WIDTH = 640
HEIGHT = 360
COLOR = (57, 255, 20)
THICKNESS = 3

def main():
    root = tk.Tk()
    root.title("Cube")
    root.resizable(width=False, height=False)

    image = Image.new('RGB', (WIDTH, HEIGHT))
    label = tk.Label(root)

    points = []
    for i in range(8):
        s = format(i, "03b")  # Zero-padded binary representation of i.
        points.append(Vector([float(d) - 0.5 for d in s]))

    draw = ImageDraw.Draw(image)

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

        angle += 0.004


def draw_cube(points, image, angle):
    cos, sin = math.cos(angle), math.sin(angle)
    rx = Matrix([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
    ry = Matrix([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
    rz = Matrix([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    rotation = rx * ry * rz

    projected = []
    for vector in points:
        rotated = rotation * vector
        dist = 2
        z = 1 / (dist - rotated.z)
        projection = Matrix([[z, 0, 0], [0, z, 0]])
        projected.append((projection * rotated) * (WIDTH / 2))

    image.rectangle((0, 0, WIDTH, HEIGHT), 0) # Clear screen.

    for i in range(4):
        connect(projected[i], projected[i + 4], image)

    for i in range(0, 8, 2):
        connect(projected[i], projected[i + 1], image)

    for i in range(2):
        connect(projected[i], projected[i + 2], image)
        connect(projected[i + 4], projected[i + 6], image)


def connect(v1, v2, image):
    x1, y1 = v1
    x2, y2 = v2
    x1, x2 = x1 + WIDTH / 2, x2 + WIDTH / 2
    y1, y2 = y1 + HEIGHT / 2, y2 + HEIGHT / 2
    
    image.line((x1, y1, x2, y2), fill=COLOR, width=THICKNESS)


if __name__ == "__main__":
    main()
