import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
from linalg import Vector, Matrix

WIDTH = 640
HEIGHT = 360
COLOR = (57, 255, 20)
THICKNESS = 2

def main():
    root = tk.Tk()
    root.title("Tesseract")
    root.resizable(width=False, height=False)

    image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    label = tk.Label(root, image=ImageTk.PhotoImage(image=Image.fromarray(image)))

    points = []
    for i in range(16):
        s = format(i, "04b")  # Zero-padded binary representation of i.
        points.append(Vector([float(d) - 0.5 for d in s]))

    angle = 0.0
    while True:
        cube(points, image, label, angle)
        root.update_idletasks()
        root.update()

        angle += 0.004


def cube(points, image, label, angle):
    cos, sin = np.cos(angle), np.sin(angle)
    rxy = Matrix([[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    rzw = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, cos, -sin], [0, 0, sin, cos]])
    rx = Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])  # PI / 2 Rotation about X-axis

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

        projected.append(projected_2d * WIDTH)

    image[:] = 0  # Clear screen.

    for i in range(4):
        connect(projected[i], projected[i + 4], image)
        connect(projected[i + 8], projected[i + 12], image)

    for i in range(0, 8, 2):
        connect(projected[i], projected[i + 1], image)
        connect(projected[i + 8], projected[i + 9], image)

    for i in range(2):
        connect(projected[i], projected[i + 2], image)
        connect(projected[i + 8], projected[i + 10], image)
        connect(projected[i + 4], projected[i + 6], image)
        connect(projected[i + 12], projected[i + 14], image)

    for i in range(8):
        connect(projected[i], projected[i + 8], image)

    # Update screen.
    frame_image = ImageTk.PhotoImage(image=Image.fromarray(image))
    label.configure(image=frame_image)
    label.image = frame_image
    label.pack()


def connect(v1, v2, image):
    x1, y1 = v1
    x2, y2 = v2
    x1, x2 = x1 + WIDTH / 2, x2 + WIDTH / 2
    y1, y2 = y1 + HEIGHT / 2, y2 + HEIGHT / 2
    cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), COLOR, THICKNESS)


if __name__ == "__main__":
    main()
