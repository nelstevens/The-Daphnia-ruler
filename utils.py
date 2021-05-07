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

# create function to erode mask
def erode_mask(edges, props, gray):
    # reformat edges to work with opencv
    edges = np.uint8(edges)
    edges_res = edges
    kernel_size = 2
    # continue opening until solidity fits
    while props[0].solidity < 0.93:
        edges_res = edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        edges_res = cv2.morphologyEx(edges_res, cv2.MORPH_OPEN, kernel, iterations = 1)

        # relabel imageregions and calculate properties
        label_img = morphology.label(edges_res, connectivity=2, background=0)
        props = measure.regionprops(label_img, gray)
        props = sorted(props, reverse=True, key=lambda k: k.area)
        kernel_size += 1
    # create list with results
    res = [props, edges_res, label_img]
    # return results
    return(res)

# create function to plot binary image
def plt_binary(edges_res, label_img, props):
    '''
    creates binary image in numpy format
    '''
    # make array of zeros
    bw_img = 0*edges_res
    # crop to largest object
    bw_img = (label_img) == props[0].label
    # copy image
    bw_img_all = bw_img.copy()
    # fill roi
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    # transform to numpy array
    binary2 = np.uint8(255*bw_img_all)
    # return binary array
    return(binary2)