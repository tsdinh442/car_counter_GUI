import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_drawer import ImageDrawer

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDrawer(root)
    root.mainloop()