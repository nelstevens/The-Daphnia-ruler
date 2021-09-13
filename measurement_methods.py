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
import utils
import json
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

    # import and resize
    img_res = utils.import_image(image)

    # define output into different variables
    img = img_res["img"]
    gray = img_res["gray"]
    scf = img_res["scf"]

    # create mask
    edges = utils.create_mask(gray)

    # create regionproperties
    props = utils.create_props(edges, gray)

    # erode mask and return new properties
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # plot binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # plot mask contour on image
    img = utils.plt_contour(binary2, img)

    # plot elipse on image
    img = utils.plt_elipse(img, props)
    
    # plot major axis of fitted elipse
    img = utils.plt_majaxis(img, props)
    
    # plot minor axis of fitted elipse
    img = utils.plt_minaxis(img, props)
    
    # make dictionary with resuls
    res = utils.make_res(img, props, scf, image)

    # return results
    return(res)




# define function that uses landmarks to calculate body size
# also discard background while detecting eye
def eye_method_2(image):
    ''' This method uses the eye of the daphnia as a landmark
    and calculates the distance to the base of the tail, the length of the tail,
    and the angle between the tail and the body
    input:
        image source
    output: dictionary with 8 values:
        output['ID'] : ID of the image
        output['eye.length'] = Length from eye to base of tail
        output['perimeter'] = perimeter os binary mask
        output['area'] = area of binary mask
        output['minor'] = minor axis of fitted elipse
        output['solidity'] = ratio of the area of the binary mask
        and the area of the convex hull
        output['full.Length'] = major axis length of the fitted elipse
        output['tail.Length'] = the length of the tail_length
        output['tail.angle'] = the angle between the tail and the line between
        eye and the base of the tail
        output['image'] = imgage with plotted size estimate'''

    # import and resize
    img_res = utils.import_image(image)

    # define output into different variables
    img = img_res["img"]
    gray = img_res["gray"]
    scf = img_res["scf"]

    # create mask
    edges = utils.create_mask(gray)

    # create regionproperties
    props, label_img = utils.create_props(edges, gray, eyeMethod = True)

    # define uneroded binary image
    binary1 = utils.plt_binary(edges, label_img, props)

    # erode mask and return new properties
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # plot binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # get major and minor axis
    major = props[0].major_axis_length
    minor = props[0].minor_axis_length

    # add perimeter of mask
    perimeter = props[0].perimeter

    # add area of mask
    area = props[0].area

    # add solidity (proportion of the pixels in shape to the pixels in the convex hull)
    solidity = props[0].solidity


    # find eye in mask
    cX, cY = utils.find_eye(binary2, img)

    # find tip of tail and length between eye and tip
    far_x, far_y, daphnia_Length_eye_tip = utils.find_tip(binary1, cX, cY)

    # find base, angle and daphnia length
    base_x, base_y, daphnia_Length, angle, contours, tail_Length = utils.find_base(binary2, far_x, far_y, cX, cY, daphnia_Length_eye_tip)
    
    # plot mask contour on image
    img = utils.plt_contour(binary2, img)

    # plot elipse on image
    cv2.ellipse(img, (int(props[0].centroid[1]), int(props[0].centroid[0])),
                (int(props[0].major_axis_length/2), int(props[0].minor_axis_length/2)),
                (-props[0].orientation*180/pi+90), 0, 360, 0, 0)

    # # plot major axis of fitted elipse
    # get deltas
    dx = (props[0].major_axis_length/2)*math.sin(props[0].orientation-(math.pi/2))
    dy = (props[0].major_axis_length/2)*math.cos(props[0].orientation-(math.pi/2))

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
    dx = (props[0].minor_axis_length/2)*math.sin(props[0].orientation)
    dy = (props[0].minor_axis_length/2)*math.cos(props[0].orientation)

    # get start
    x1 = props[0].centroid[0]-dx
    y1 = props[0].centroid[1]+dy

    # get end
    x2 = props[0].centroid[0]+dx
    y2 = props[0].centroid[1]-dy

    # plot line
    cv2.line(img, (int(y2), int(x2)), (int(y1), int(x1)), (255, 0, 255), 2)

    # plot tail on image
    cv2.line(img, (far_x,far_y),(base_x, base_y), (255, 0, 0), 2)

    # plot daphnia Length on image (from eye to base)
    cv2.line(img, (cX, cY), (base_x, base_y), (0, 0, 255), 2)

    # Create ID for image with image number and base directory
    imgnum = os.path.basename(image)
    imgdir = image.split(os.path.sep)[-2]
    ID = os.path.join(imgdir, imgnum)

    # scale measurements back to original image size where necessary
    tail_Length = tail_Length/scf
    daphnia_Length = daphnia_Length/scf
    perimeter = perimeter/scf
    area = area / scf**2
    minor = minor/scf
    major = major/scf


    # # create dictionary with results
    res = {}
    res['ID'] = ID
    res['tail.Length'] = tail_Length
    res['image'] = img
    res['eye.Length'] = daphnia_Length
    res['perimeter'] = perimeter
    res['area'] = area
    res['minor'] = minor
    res['solidity'] = solidity
    res['full.Length'] = major
    res['tail.angle'] = angle

    # return results
    return(res)


# if called directly show image output of all three methods
if __name__ == '__main__':
    res1 = head_method(sys.argv[1])
    try:
        res3 = eye_method_2(sys.argv[1])
        cv2.imshow('eye method 2', res3['image'])
    except:
        print('Eye detetion failed!')
    cv2.imshow('head method', res1['image'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
