import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from car_counter import ImageDrawer
from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO('models/car_detector.pt')
    root = tk.Tk()
    app = ImageDrawer(root, model)
    root.mainloop()