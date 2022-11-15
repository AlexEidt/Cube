import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from linalg import Vector, Matrix

WIDTH = 640
HEIGHT = 360
COLOR = (57, 255, 20)
THICKNESS = 3
CENTER = Vector([WIDTH / 2, HEIGHT / 2])

def main():
    root = tk.Tk()
    root.title("Tesseract")
    root.resizable(width=False, height=False)

    image = Image.new('RGB', (WIDTH, HEIGHT))
    label = tk.Label(root)

    points = []
    for i in range(16):
        s = format(i, "04b")  # Zero-padded binary representation of i.
        points.append(Vector([float(d) - 0.5 for d in s]))

    draw = ImageDraw.Draw(image)

    stop = []
    root.protocol("WM_DELETE_WINDOW", lambda: stop.append(0))

    angle = 0.0
    while not stop:
        draw_tesseract(points, draw, angle)

        # Update screen.
        ph_image = ImageTk.PhotoImage(image)
        label.configure(image=ph_image)
        label.image = ph_image
        label.pack()

        root.update_idletasks()
        root.update()

        angle += 0.002


def draw_tesseract(points, image, angle):
    image.rectangle((0, 0, WIDTH, HEIGHT), 0) # Clear screen.

    cos, sin = math.cos(angle), math.sin(angle)
    rxy = Matrix([[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    rzw = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, cos, -sin], [0, 0, sin, cos]])
    rx = Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]]) # PI / 2 Rotation about X-axis

    rotation = rxy * rzw

    # 4-D to 3-D to 2-D projection.
    projected = []
    for vector in points:
        rotated = rotation * vector
        dist = 2.0

        # 4-D to 3-D projection.
        w = 1 / (dist - rotated.w)
        projection = Matrix([[w, 0, 0, 0], [0, w, 0, 0], [0, 0, w, 0]])
        projected_3d = rx * (projection * rotated)

        # 3-D to 2-D projection.
        z = 1 / (dist - projected_3d.z)
        projection = Matrix([[z, 0, 0], [0, z, 0]])
        projected_2d = projection * projected_3d

        projected.append(projected_2d * WIDTH + CENTER)

    for i in range(4):
        image.line((*projected[i], *projected[i + 4]), fill=COLOR, width=THICKNESS)
        image.line((*projected[i + 8], *projected[i + 12]), fill=COLOR, width=THICKNESS)

    for i in range(0, 8, 2):
        image.line((*projected[i], *projected[i + 1]), fill=COLOR, width=THICKNESS)
        image.line((*projected[i + 8], *projected[i + 9]), fill=COLOR, width=THICKNESS)

    for i in range(2):
        image.line((*projected[i], *projected[i + 2]), fill=COLOR, width=THICKNESS)
        image.line((*projected[i + 8], *projected[i + 10]), fill=COLOR, width=THICKNESS)
        image.line((*projected[i + 4], *projected[i + 6]), fill=COLOR, width=THICKNESS)
        image.line((*projected[i + 12], *projected[i + 14]), fill=COLOR, width=THICKNESS)

    for i in range(8):
        image.line((*projected[i], *projected[i + 8]), fill=COLOR, width=THICKNESS)


if __name__ == "__main__":
    main()
