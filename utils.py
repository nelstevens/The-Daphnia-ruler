# import libraries
import os
import cv2
import numpy as np
import sys
from math import pi
from skimage import morphology, measure
from skimage.filters import scharr
from scipy import ndimage
import math
import copy
import warnings
# Create function to load image in proper format
def import_image(image):
    '''
    imports and resizes image
    '''
    # Load in rayscale, resize
    img = cv2.imread(image)
    # save aspect ratio
    height, width = np.shape(img)[0:2]

    # scale image to 720p width
    scf = 720/width
    nwidth = 720
    nheight = int(height * scf)
    img = cv2.resize(img, (nwidth, nheight))

    # export image
    return(img)

# write function to grayscale image
def grayscale_image(img):
    '''
    exports image to grayscale
    '''
    # grayscale image
    gray = np.uint8(np.mean(img, 2))

    # export grayscale
    return(gray)