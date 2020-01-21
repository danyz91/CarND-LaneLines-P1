# **Finding Lane Lines on the Road** 

[//]: # (Image References)

[img_tuning_gui]: ./writeup_img/tuning_gui.png "Tuning Gui complete"
[img_tuning_gui_canny]: ./writeup_img/tuning_gui_canny.png "Tuning Gui with canny result displayed"
[img_roi]: ./writeup_img/roi.jpg "Region of interest visualization"

---

### Reflection

### 1. Pipeline description

#### Pipeline
My pipeline is represented by the function ```lane_extraction_pipeline()``` that takes in input an image and return the same image with the detected lane printed on it
The pipeline consists of 5 steps:

1. Grayscale conversion
2. Gaussian smoothing 
3. Canny edge detector
4. Region of interest extraction
5. Hough Transform

Firstly I focused in region of interest shape and coordinates. 
I finally decided for a trapezoidal shape represented in the following example image:
![alt text][img_roi]

#### Parameters tuning
In the whole pipeline there are 8 parameters to tune:

Algorithm | Parameter | 
------------ | ------------
Gaussian Smoothing | **kernel size** 
Canny Detector |  **low threshold**
Canny Detector |  **high threshold**
Hough Transform |  **rho** 
Hough Transform |  **theta** 
Hough Transform |  **intersection threshold**
Hough Transform |  **min line length**
Hough Transform  | **max line gap**

In order to tune them effectively I decided to create a tuning GUI contained into tuning_gui folder of this repository. The GUI is made using opencv visualization library.
The folder tuning_gui is composed by three files:

1. **cv_lib.py** containing the functions originally present in notebook provided
2. **cv_lane_detector.py** containing the wrapper function ```lane_extaction_pipeline``` previously defined
3. **tuning_gui.py** where there is the main GUI code. This scripts accepts two command line parameters
```
  -d, --dir                       Directory where to find test images
  -s, --step {0,1,2,3,4,5}        Step number whose output will be plotted in GUI. 0 for all pipeline
```

With the tuning GUI it is possible to visualize pipeline total result or the intermediate result of a single step via the corresponding parameter.

![alt text][img_tuning_gui_canny]![alt text][img_tuning_gui]

When the GUI is closed the program will print in the terminal the final value of the parameters used.

Final parameters used:

Algorithm | Parameter | Value
------------ | ------------ | -------------
Gaussian Smoothing  |  **kernel size** | 7
Canny Detector |  **low threshold** | 80
Canny Detector |  **high threshold** | 160
Hough Transform |  **rho** | 2
Hough Transform |  **theta** | 1 rad
Hough Transform |  **intersection threshold** | 15
Hough Transform |  **min line length** | 10
Hough Transform |  **max line gap** | 10

#### Single line extraction
In order to draw a single line on the left and right lanes, I modified the draw_lines() function by:

1. Grouping the lines by their slope and their position. 
Lines on left half of the image and with a slope < 0 are grouped for left side line.
Lines on right half of the image and with a slope > 0 are grouped for right side line.
2. Choosing the dominant line for each of the two groups.
Dominant line is defined as the line that passed through the average between all the points of a group and through the two bases of the trapezoid of the ROI. These two points are computed using the equation:
```
y-y_average = slope*(x-x_average)
```
with y equals to the two value of the ROI trapezoid bases

### 2. Identify potential shortcomings with your current pipeline

- One potential shortcoming is the shape of the region of interest chosen. This is quite fitted to single straight lane and it would suffer in dealing with curves.

### 3. Suggest possible improvements to your pipeline

- Add ROI shape editing into tuning GUI. In this way it would be possible to customize also the geometrical shape of region of interest extracted. 
- Freeze single parameters when the user decide to fix its value. 
- Save last parameters value to a file.

