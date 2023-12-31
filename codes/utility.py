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

import numpy as np
import cv2

def masking(image, polygons, opacity):

    '''
    Parameters
    ----------
    image: str - path to an image
    polygons: list - list of vertices (x, y)
    opacity: float - opacity value

    Return: np array - image with mask overlaid
    -------
    '''

    # create a blank white image with same dimension as the org image
    blank = np.ones_like(image, dtype=np.uint8) * 255

    # create a blank black image with the same dimension as the ori image
    mask = np.zeros_like(image, dtype=np.uint8)

    # fill the polygon with white color on the blank black image
    cv2.fillPoly(mask, polygons, (255, 255, 255))

    # blend the mask image with the original image
    blended = cv2.addWeighted(src1=image, alpha=opacity, src2=blank, beta=1 - opacity, gamma=0)

    # perform masking
    result = cv2.bitwise_and(blended, 255 - mask) + cv2.bitwise_and(image, cv2.bitwise_not(255 - mask))


    return result
