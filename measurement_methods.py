# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:21:59 2019

@author: Nelson
"""
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

# create function that does not require landmarks
def head_method(image):
    ''' This method calculates the Length of the major axis of a fitted ellipse
    around the binary mask of the daphnia
    input:
        image source
    output: dictionary with 8 values:
        output['ID'] : ID of the image
        output['perimeter'] = perimeter os binary mask
        output['area'] = area of binary mask
        output['minor'] = minor axis of fitted elipse
        output['solidity'] = ratio of the area of the binary mask
        and the area of the convex hull
        output['full.Length'] = major axis length of the fitted elipse
        output['image'] = imgage with plotted size estimate'''
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

    # create mask
    edges_mag = scharr(gray)
    edges_med = np.median(edges_mag)
    edges_thresh = 2.5*edges_med
    edges = edges_mag >= edges_thresh
    edges = morphology.closing(edges, morphology.square(3))
    edges = ndimage.binary_fill_holes(edges)
    edges = morphology.erosion(edges, morphology.square(3))

    # label imageregions and calculate properties
    label_img = morphology.label(edges, neighbors=8, background=0)
    props = measure.regionprops(label_img, gray, coordinates = 'xy')
    props = sorted(props, reverse=True, key=lambda k: k.area)

    ## erode the mask
    # reformat edges to work with opencv
    edges = np.uint8(edges)
    edges_res = edges
    kernel_size = 2
    # continue opening until solidity fits
    while props[0].solidity < 0.93:
        edges_res = edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        edges_res = cv2.morphologyEx(edges_res, cv2.MORPH_OPEN, kernel, iterations = 1)

        # label imageregions and calculate properties
        label_img = morphology.label(edges_res, neighbors=8, background=0)
        props = measure.regionprops(label_img, gray, coordinates = 'xy')
        props = sorted(props, reverse=True, key=lambda k: k.area)
        kernel_size += 1

    # plot binary image
    bw_img = 0*edges_res
    bw_img = (label_img) == props[0].label
    bw_img_all = bw_img.copy()
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    binary2 = np.uint8(255*bw_img_all)

    # plot mask contour on image
    contours, hierarchy = cv2.findContours(binary2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

    # plot elipse on image
    cv2.ellipse(img, (int(props[0].centroid[1]), int(props[0].centroid[0])),
                (int(props[0].major_axis_length/2), int(props[0].minor_axis_length/2)),
                -props[0].orientation*180/pi, 0, 360, 0, 0)

    # # plot major axis of fitted elipse
    # get deltas
    dx = (props[0].major_axis_length/2)*math.sin(props[0].orientation)
    dy = (props[0].major_axis_length/2)*math.cos(props[0].orientation)

    # get start
    x1 = props[0].centroid[0]-dx
    y1 = props[0].centroid[1]+dy

    # get end
    x2 = props[0].centroid[0]+dx
    y2 = props[0].centroid[1]-dy

    # plot line
    cv2.line(img, (int(y2), int(x2)), (int(y1), int(x1)), (0, 255, 0), 2)

    # # plot minor axis of fitted elipse
    # get deltas
    dx = (props[0].minor_axis_length/2)*math.sin(props[0].orientation-(math.pi/2))
    dy = (props[0].minor_axis_length/2)*math.cos(props[0].orientation-(math.pi/2))

    # get start
    x1 = props[0].centroid[0]-dx
    y1 = props[0].centroid[1]+dy

    # get end
    x2 = props[0].centroid[0]+dx
    y2 = props[0].centroid[1]-dy

    # plot line
    cv2.line(img, (int(y2), int(x2)), (int(y1), int(x1)), (255, 0, 255), 2)

    # get major and minor axis
    major = props[0].major_axis_length
    minor = props[0].minor_axis_length

    # add perimeter of mask
    perimeter = props[0].perimeter

    # add area of mask
    area = props[0].area

    # add solidity (proportion of the pixels in shape to the pixels in the convex hull)
    solidity = props[0].solidity

    # Create ID for image with image number and base directory
    imgnum = os.path.basename(image)
    imgdir = image.split(os.path.sep)[-2]
    ID = os.path.join(imgdir, imgnum)

    # scale measurements back to original image size where necessary
    perimeter = perimeter/scf
    area = area / scf**2
    minor = minor/scf
    major = major/scf

    # create dictionary with results
    res = {}
    res['ID'] = ID
    res['perimeter'] = perimeter
    res['area'] = area
    res['minor'] = minor
    res['solidity'] = solidity
    res['full.Length'] = major
    res['image'] = img

    # return results
    return(res)

