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
    img = utils.plt_elipse(img, props)

    # plot major axis of fitted elipse
    img = utils.plt_majaxis(img, props)
    
    # plot minor axis of fitted elipse
    img = utils.plt_minaxis(img, props)

    # plot tail on image
    img = utils.plt_tail(img, far_x, far_y, base_x, base_y)

    # plot daphnia Length on image (from eye to base)
    img = utils. plt_length(img, cX, cY, base_x, base_y)

    # create dictionary with results
    res = utils.make_res(
        img = img,
        props = props,
        scf = scf,
        image = image,
        eyeMethod = True,
        tail_Length = tail_Length,
        daphnia_Length = daphnia_Length,
        angle = angle
    )

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
