import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from utility import get_centroid, display_number_of_cars
from predict import predict

STROKE = 3

class ImageDrawer:
   def __init__(self, root, model):
       self.root = root
       self.root.title("Car Counter")
       # Initialize image
       self.image = None
       self.drawn_image = None
       # Create canvas
       self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
       self.canvas.pack()
       # Set up UI
       self.load_button = tk.Button(root, text="Select Images", command=self.load_image)
       self.load_button.pack(side=tk.LEFT, padx=5, pady=10)
       self.clear_button = tk.Button(root, text="Clear", command=self.clear_polygons)
       self.clear_button.pack(side=tk.LEFT, padx=5, pady=10)

       self.next_button = tk.Button(self.root, text="Next", command=self.show_next_image)
       self.next_button.pack_forget()

       self.prev_button = tk.Button(self.root, text="Previous", command=self.show_prev_image)
       self.prev_button.pack_forget()

       #self.count_cars = tk.Button(root, text="Count cars", command=self.predict)
       #self.count_cars.pack_forget()

       # Init polygons vertices
       self.points = []
       self.polygons = []
       # Set up mouse event handling
       self.canvas.bind("<Button-1>", self.draw_polygon)

       # load model
       self.model = model



   def load_image(self):
       self.file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png *.jpg *.jpeg")])

       if self.file_paths:
           self.current_image_index = 0
           self.show_additional_buttons()

           self.fit_image_to_frame()
           self.drawn_image = np.copy(self.image)
           self.display_image()


           # Reset polygons vertices
           self.points = []
           self.polygons = [[] for i in range(len(self.file_paths))]
           self.predicted_image = [None for i in range(len(self.file_paths))]

   def fit_image_to_frame(self):
       image = cv2.imread(self.file_paths[self.current_image_index])
       # fit the image to the canvas
       image_height, image_width, _ = image.shape
       width, height = self.canvas.winfo_width(), self.canvas.winfo_height()

       scale = width / image_width
       self.image = cv2.resize(image, (int(image_width * scale), int(image_height * scale)))

   def show_additional_buttons(self):
       self.check_image_index()
       self.next_button.pack(side=tk.RIGHT, padx=5, pady=10)
       self.prev_button.pack(side=tk.RIGHT, padx=5, pady=10)
       #self.count_cars.pack(side=tk.LEFT, padx=5, pady=10)


   def check_image_index(self):

       self.prev_button.config(state='normal')
       self.next_button.config(state='normal')

       if self.current_image_index == 0:
           if self.current_image_index == len(self.file_paths) - 1:
               self.next_button.config(state='disabled')
           self.prev_button.config(state='disabled')

       elif self.current_image_index == len(self.file_paths) - 1:
           self.next_button.config(state='disabled')


   def show_next_image(self):
       self.current_image_index += 1
       self.check_image_index()

       #self.polygons_image = np.copy(self.image)
       if self.current_image_index < len(self.file_paths):
           self.fit_image_to_frame()
           current_image = self.predicted_image[self.current_image_index]
           self.drawn_image = current_image if current_image is not None else np.copy(self.image)
           self.display_image()
           #return self.image

   def show_prev_image(self):
       self.current_image_index -= 1
       self.check_image_index()

       if self.current_image_index < len(self.file_paths):
           self.fit_image_to_frame()
           current_image = self.predicted_image[self.current_image_index]
           self.drawn_image = current_image if current_image is not None else np.copy(self.image)
           self.display_image()
           #return self.image

   def closing_polygon(self, point_first, point_last):
       thresh = 30
       if np.linalg.norm(np.array(point_first) - np.array(point_last)) < thresh:
           return True
       return False

   def draw_polygon(self, event):
       if self.image is not None:
           x, y = event.x, event.y
           if len(self.points) == 0:
               cv2.circle(self.drawn_image, (x, y), STROKE, (0, 255, 0), -1)
               self.points.append((x, y))
           else:
               cv2.line(self.drawn_image, self.points[-1], (x, y), (0, 255, 0), STROKE)
               self.points.append((x, y))

           if len(self.points) > 3:
               if self.closing_polygon(self.points[0], (x, y)):
                   self.drawn_image = np.copy(self.image)
                   self.polygons[self.current_image_index].append(self.points)

                   self.points = []
                   self.predict()

           self.display_image()

   def clear_polygons(self):
       if self.image is not None:
           self.drawn_image = np.copy(self.image)
           self.polygons[self.current_image_index] = []
           self.points = []
           self.display_image()

   def predict(self):

       for polygon in self.polygons[self.current_image_index]:

           cv2.polylines(self.drawn_image, np.array([polygon[:-1]]), True, (0, 255, 255), STROKE)
           # detecting cars and start counting
           count, centers, bboxes, scores = predict(self.model, np.array(polygon), self.image, conf=0.7, iou=0.7)

           # mark each car with a dot
           for center in centers:
               cv2.circle(self.drawn_image, center, radius=4, color=(0, 0, 255), thickness=-1)

           # display the number of cars
           display_number_of_cars(self.drawn_image, centroid=get_centroid(polygon), number_of_cars=count)

       self.predicted_image[self.current_image_index] = self.drawn_image

       #self.display_image()



   def display_image(self):
       if self.image is not None:
           # Convert image from BGR to RGB for Tkinter
           image_rgb = cv2.cvtColor(self.drawn_image, cv2.COLOR_BGR2RGB)

           # Convert to PhotoImage format
           image_tk = Image.fromarray(image_rgb)
           image_tk = ImageTk.PhotoImage(image_tk)

           # Update canvas
           self.canvas.config()
           self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
           self.canvas.image = image_tk

