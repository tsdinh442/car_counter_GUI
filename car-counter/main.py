import tkinter as tk
from car_counter import ImageDrawer
from ultralytics import YOLO


if __name__ == "__main__":
    car_detector = 'models/car-detector.pt'  # replace your model here
    model = YOLO(car_detector)
    root = tk.Tk()
    app = ImageDrawer(root, model)
    root.mainloop()