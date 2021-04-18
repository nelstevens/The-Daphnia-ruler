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
    imports, resizes and grayscales image.
     returns additional info on image.
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

    # grayscale image
    gray = np.uint8(np.mean(img, 2))

    # create dictionary with results
    res = {}
    res["img"] = img
    res["gray"] = gray
    res["scf"] = scf

    # export image
    return(res)
    
# create function that creates mask
def create_mask(gray):
    '''
    masks grayscaled image
    '''
    edges_mag = scharr(gray)
    edges_med = np.median(edges_mag)
    edges_thresh = 2.5*edges_med
    edges = edges_mag >= edges_thresh
    edges = morphology.closing(edges, morphology.square(3))
    edges = ndimage.binary_fill_holes(edges)
    edges = morphology.erosion(edges, morphology.square(3))

    # return edges
    return(edges)

# create function to label imageregions and calculate properties
def create_props(edges, gray):
    '''
    labels image and defines properties
    '''
    # label imageregions and calculate properties
    label_img = morphology.label(edges, connectivity=2, background=0)
    props = measure.regionprops(label_img, gray)
    props = sorted(props, reverse=True, key=lambda k: k.area)

    # return properties
    return(props)
