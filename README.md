# Car Counter GUI

Object detection has been extensively used in car counting, and this project takes a user-friendly approach to enhance its application. The goal is to simplify the process, allowing users to easily draw polygons on images. This feature enables them to target specific areas and only count cars that are within the regions of interest.

The project leverages Tkinter, a built-in library in Python, to create buttons, facilitating an intuitive and interactive user interface.

<br/><br/>

### Video Demo

[![Video](https://img.youtube.com/vi/ZT7juY0WXYU/0.jpg)](https://www.youtube.com/watch?v=ZT7juY0WXYU)

<br/><br/>

### Getting started

Follow the instructions below to get the application up and running (currently for MacOS only).

* Setting up environment 
<br/><br/>
`conda create --name car-counter python=3.10`
<br/><br/>
* Installing requirements
<br/><br/>
`    conda install ultralytics \n
     conda install pytorch torchvision torchaudio -c pytorch -c conda-forge
`
<br/><br/>
To learn more about YOLOv8 --> https://github.com/ultralytics/ultralytics
<br/><br/>

* Place your own detection model 
<br/><br/>
`Go to the 'models' directory and place the detection model there. Name it as 'car-detector.pt'`
<br/><br/>

* Run app
<br/><br/>
`python codes/main.py`

<br/><br/>

### How it works

* First, it performs car detection on the entire image
<br/><br/>
    - The results are bounding boxes of all the cars the model is able to detect.
    <br/><br/>
    `x1, y1, x2, y2, score, class_id = detection` 
    <br/><br/>
    (x1, y1) is the North West corner while (x2, y2) is the South East corner of the bounding box.
    <br/><br/>

    - Caculating the centroids of these boxes
    <br/><br/>
    `centroid = (int((x1 + x2) / 2), int((y1 + y2) / 2))`

<br/>

* Then, we select only centroids that are inside the polygons and output the count
<br/><br/>
    - using pointPolygonTest by OpenCV to test each centroid
    <br/><br/>
    `check = cv2.pointPolygonTest(targeted_regions, centroid, measureDist=False)`

<br/><br/>

### License

GNU General Public License 3.0
