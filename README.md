# The-Daphnia-ruler
Automatically collect morphometric traits of Daphnia

![](images/final_product_fin.jpg)
## Overview
The Daphnia ruler is a set of python scripts that can measure morphometric traits of Daphnia
from images taken under a microscope. The following traits are measured:
* body size: measured from the center of the eye to the base of the tail
* body size: approximated by fitting an ellipse around the Daphnia body
* tail length
* tail angle
* body area
* body perimeter
* body width
* solidity

## Installation
The fastest way to get your system setup is to make sure you've installed python 3 (https://www.python.org/) and clone this repository to your local drive.
Once complete use the package manager pip to install the necessary dependencies:
1. Open your command prompt and navigate to the cloned directory
2. Run this command: 
```bash
pip install -r requirements.txt
```
Users who wish to install dependencies manually run:
```bash
pip install opencv-python
pip install scikit-image
pip install pandas
pip install tqdm
```
## Quickstart
The fastest way to get your system setup is to install Anaconda 
and then add the opencv3 module through conda:

1. Install Anaconda for python 2.7 from https://anaconda.org/
2. Open a terminal and install the required python module: 
* $ conda install -c menpo opencv3
* $ conda install scipy
3. Place both measurement_methods.py and daily_measurement.py in a directory that contains subfolder(s)
with the original images.
4. Make sure the names of folders containing images start with: daphnia_images
5. Open a terminal and navigate to the directory containing both python scripts
6. Run this command: $ python measure_daphnia.py

The program will now create subdirectories within image folders, containing a copy of each image with
measurements overplotted. Additionaly there will be a .txt file containing all measurements in pixel.

## Requirements
* Python2.7, numpy, scipy, skimage, opencv3
* tested only on windows (thus far)

## Detailed desription
The Daphnia ruler is designed to measure morphological features of Daphnia from images taken under
a microscope. Although the Daphnia ruler can handle some noise in the image, it is crucial to
minimize background noise (scratches on microscope slide etc.). In rare cases the body size measurement
from the center of the eye to the base of the tail fails, and tail length fails.
In such cases the corresponding fields in the text file contain NA's. Each row in the text file will
start with an image ID, which corresponds to the name of the image file. Output images with features
overplotted are in .png format.

## Author
* Nelson Stevens
* Contact: nelson.stevens92@gmail.com
