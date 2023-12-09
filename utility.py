import cv2
import numpy as np

box_color = (0, 0, 0)
txt_color = (255, 255, 255)

def get_centroid(polygon):

    centroid = np.mean(np.array(polygon), axis=0)  # centroid of the polygon
    return centroid.astype(int)
def display_number_of_cars(image, centroid, number_of_cars, font=cv2.FONT_HERSHEY_SIMPLEX):

    X_PADDING = 5
    Y_PADDING = 5

    txt = str(number_of_cars) + ' cars'
    txt_size_x, txt_size_y = cv2.getTextSize(txt, font, fontScale=1, thickness=1)[0]

    x_0 = int(centroid[0] - (txt_size_x / 2)) - X_PADDING
    y_0 = int(centroid[1] - (txt_size_y / 2)) - Y_PADDING

    txt_position = (x_0 + X_PADDING, y_0 + Y_PADDING + txt_size_y)

    cv2.rectangle(image, (x_0, y_0), (x_0 + txt_size_x + (X_PADDING * 2), y_0 + txt_size_y + (Y_PADDING * 2)), box_color, thickness=-1)
    cv2.putText(image, txt, txt_position, cv2.FONT_HERSHEY_SIMPLEX, 1, color=txt_color, thickness=2)
