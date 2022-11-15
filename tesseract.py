
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
from matrix import Vector, Matrix

WIDTH = 640
HEIGHT = 360


def main():
    root = tk.Tk()
    root.title('Cube')
    root.resizable(width=False, height=False)

    image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
    label = tk.Label(root, image=frame_image)
    label.pack()

    points = []
    for i in range(8):
        s = format(i, '03b')
        points.append(Vector([float(d) - 0.5 for d in s]))

    angle = 0.0
    while True:
        cube(points, image, label, angle)
        root.update_idletasks()
        root.update()
        angle += 0.001


def cube(points, image, label, angle):
    cos, sin = np.cos(angle), np.sin(angle)
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
        projected.append((projection * rotated) * 300)

    image[:] = 0

    connect(0, 4, projected, image)
    connect(1, 5, projected, image)
    connect(2, 6, projected, image)
    connect(3, 7, projected, image)

    connect(0, 1, projected, image)
    connect(2, 3, projected, image)
    connect(4, 5, projected, image)
    connect(6, 7, projected, image)

    connect(0, 2, projected, image)
    connect(1, 3, projected, image)
    connect(4, 6, projected, image)
    connect(5, 7, projected, image)

    update(image, label)


def connect(i, j, arr, image):
    a = int(arr[i].x) + WIDTH // 2
    b = int(arr[i].y) + HEIGHT // 2
    c = int(arr[j].x) + WIDTH // 2
    d = int(arr[j].y) + HEIGHT // 2
    cv2.line(image, (a, b), (c, d), (57, 255, 20), 2)


def update(image, label):
    frame_image = ImageTk.PhotoImage(image=Image.fromarray(image))
    label.configure(image=frame_image)
    label.image = frame_image
    label.pack()


if __name__ == '__main__':
    main()