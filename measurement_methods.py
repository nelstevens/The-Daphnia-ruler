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
def head_method(image, res_destination):
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
    # create empty output list
    out = []
    
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
    edges_thresh = 5.5*edges_med
    edges = edges_mag >= edges_thresh
    #edges = morphology.closing(edges, morphology.square(3))
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
    '''
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
    '''
    for i in range(len(props)):
        ## add size subset here with an if statement!!


        # plot binary image
        bw_img = 0*edges_res
        bw_img = (label_img) == props[i].label
        bw_img_all = bw_img.copy()
        bw_img_all = bw_img_all + ((label_img) == props[i].label)
        binary2 = np.uint8(255*bw_img_all)

        # plot mask contour on image
        contours, hierarchy = cv2.findContours(binary2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

        # plot elipse on image
        cv2.ellipse(img, (int(props[i].centroid[1]), int(props[i].centroid[0])),
                    (int(props[i].major_axis_length/2), int(props[i].minor_axis_length/2)),
                    -props[i].orientation*180/pi, 0, 360, 0, 0)

        # # plot major axis of fitted elipse
        # get deltas
        dx = (props[i].major_axis_length/2)*math.sin(props[i].orientation)
        dy = (props[i].major_axis_length/2)*math.cos(props[i].orientation)

        # get start
        x1 = props[i].centroid[0]-dx
        y1 = props[i].centroid[1]+dy

        #print particle id at number start
        cv2.putText(img, str(i), (int(y1), int(x1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
        # get end
        x2 = props[i].centroid[0]+dx
        y2 = props[i].centroid[1]-dy

        # plot line
        cv2.line(img, (int(y2), int(x2)), (int(y1), int(x1)), (0, 255, 0), 2)

        # # plot minor axis of fitted elipse
        # get deltas
        dx = (props[i].minor_axis_length/2)*math.sin(props[i].orientation-(math.pi/2))
        dy = (props[i].minor_axis_length/2)*math.cos(props[i].orientation-(math.pi/2))

        # get start
        x1 = props[i].centroid[0]-dx
        y1 = props[i].centroid[1]+dy

        # get end
        x2 = props[i].centroid[0]+dx
        y2 = props[i].centroid[1]-dy

        # plot line
        cv2.line(img, (int(y2), int(x2)), (int(y1), int(x1)), (255, 0, 255), 2)

        # get major and minor axis
        major = props[i].major_axis_length
        minor = props[i].minor_axis_length

        # add perimeter of mask
        perimeter = props[i].perimeter

        # add area of mask
        area = props[i].area

        # add solidity (proportion of the pixels in shape to the pixels in the convex hull)
        solidity = props[i].solidity

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
        # append res to output list
        out.append(res)

    cv2.imwrite(os.path.join(res_destination, os.path.basename(image)) + '.png', img)
    # return results
    return(out)

# if called directly show image output of all three methods
if __name__ == '__main__':
    #res1 = head_method(sys.argv[1])
    # cv2.imshow('head method', res1['image'])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(res1[0])