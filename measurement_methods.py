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
    label_img = morphology.label(edges, connectivity=2, background=0)
    props = measure.regionprops(label_img, gray)
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
        label_img = morphology.label(edges_res, connectivity=2, background=0)
        props = measure.regionprops(label_img, gray)
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



# define function that uses landmarks to calculate body size
def eye_method(image):
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
    # Load in rayscale, resize
    img = cv2.imread(image)
    
    # save aspect ratio
    height, width = np.shape(img)[0:2]

    # scale image to 720p width
    scf = 720/width
    nwidth = 720
    nheight = int(height * scf)
    img = cv2.resize(img, (nwidth, nheight))
    
    #grayscale image
    gray = np.uint8(np.mean(img, 2))

    # create uneroded mask
    edges_mag = scharr(gray)
    edges_med = np.median(edges_mag)
    edges_thresh = 2.5*edges_med
    edges = edges_mag >= edges_thresh
    edges = morphology.closing(edges, morphology.square(3))
    edges = ndimage.binary_fill_holes(edges)
    edges = morphology.erosion(edges, morphology.square(3))


    # label imageregions and calculate properties
    label_img = morphology.label(edges, connectivity=2, background=0)
    props = measure.regionprops(label_img, gray)
    props = sorted(props, reverse=True, key=lambda k: k.area)

    # define uneroded binary image
    bw_img = 0*edges
    bw_img = (label_img) == props[0].label
    bw_img_all = bw_img.copy()
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    binary1 = np.uint8(255*bw_img_all)

    # # erode the mask
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
        label_img = morphology.label(edges_res, connectivity=2, background=0)
        props = measure.regionprops(label_img, gray)
        props = sorted(props, reverse=True, key=lambda k: k.area)
        kernel_size += 1

    # get binary image of eroded mask
    bw_img = 0*edges_res
    bw_img = (label_img) == props[0].label
    bw_img_all = bw_img.copy()
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    binary2 = np.uint8(255*bw_img_all)

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

    # # filter by black color
    full_black = np.array([0, 0, 0])
    half_black = np.array([100, 100, 100])

    # filter with broad spectrum
    black = cv2.inRange(img, full_black, half_black)
    eye_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(2), int(2)))
    black_eroded = cv2.morphologyEx(black, cv2.MORPH_OPEN, eye_kernel, iterations = 2)

    # define contour
    contours, hierarchy = cv2.findContours(copy.deepcopy(black_eroded), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # change thin colour spectrum until contours are of length one
    while len(contours) > 1:
        half_black = half_black - [10, 10, 10]
        black = cv2.inRange(img, full_black, half_black)
        eye_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(2), int(2)))
        black_eroded = cv2.morphologyEx(black, cv2.MORPH_OPEN, eye_kernel, iterations = 2)

        # define contour
        contours, hierarchy = cv2.findContours(copy.deepcopy(black_eroded), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    M = cv2.moments(contours[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])


    ### find tip of the tail
    # find extreme points on uneroded mask
    contours, hierarchy = cv2.findContours(copy.deepcopy(binary1), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    cnt = contours[0]

    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

    extremes = [leftmost, rightmost, topmost, bottommost]

    # save extremes and eye in a list
    points = extremes + [(cX, cY)]

    # compute distances from eye
    dxs = []
    dys = []
    lengths = []
    for i in range(len(points)):
            dy = points[i][0]-points[4][0]
            dys.append(dy)
            dx = points[i][1]-points[4][1]
            dxs.append(dx)
            L = math.sqrt(dx**2 + dy**2)
            lengths.append(L)


    # find index of max distance
    # max_dist_index = lengths.index(max(lengths))
    max_dist_index = lengths.index(max(lengths))
    # get tip of the tail(note that y,x is exchanged)
    far_x = int(cX+dys[max_dist_index])
    far_y = int(cY+dxs[max_dist_index])

    # define distance from eye to tip of tail
    daphnia_Length_eye_tip = max(lengths)

    # # find closest point of mask contour to tip of the tail (base of tail)

    # get contour of eroded mask
    contours, hierarchy = cv2.findContours(copy.deepcopy(binary2), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    # convert contours to a list
    # contours = np.ndarray.tolist(contours[0])
    contours = contours[0]
    # convert tail tip to list
    tail_tip = [far_x, far_y]



    lin_distances = np.empty(0)
    for i in range(0, len(contours)):
        con_x = contours[i][0][0]
        con_y = contours[i][0][1]
        lin_dis = math.sqrt(abs(con_x-tail_tip[0])**2 + abs(con_y-tail_tip[1])**2)
        # lin_distances.append(lin_dis)
        lin_distances = np.append(lin_distances, lin_dis)

    # find index of minimal value
    # base_index = lin_distances.index(min(lin_distances))
    base_index = np.where(lin_distances == np.min(lin_distances))[0][0]

    # find base
    base = contours[base_index]
    base_x = base[0][0]
    base_y = base[0][1]

    # define tail length
    tail_Length = np.min(lin_distances)

    # define Length of daphnia from eye to base of the tail
    daphnia_Length = math.sqrt((cX - base_x)**2 + (cY - base_y)**2)

    # find angle between tail and line from eye to base of tail
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cos_angle = (tail_Length**2 + daphnia_Length**2 - daphnia_Length_eye_tip**2)/(2*tail_Length*daphnia_Length)
        angle = math.acos(cos_angle) * (180/pi)

    # # #  plot everything
    # plot mask contour on image
    cv2.drawContours(img, contours, -1, (0,0,255), 1)

    # plot elipse on image
    cv2.ellipse(img, (int(props[0].centroid[1]), int(props[0].centroid[0])),
                (int(props[0].major_axis_length/2), int(props[0].minor_axis_length/2)),
                (-props[0].orientation*180/pi+90), 0, 360, 0, 0)

    # # plot major axis of fitted elipse
    # get deltas
    dx = (props[0].major_axis_length/2)*math.sin(props[0].orientation-(math.pi/2))
    dy = (props[0].major_axis_length/2)*math.cos(props[0].orientation-(math.pi/2))

    #  get start
    x1 = props[0].centroid[0]-dx
    y1 = props[0].centroid[1]+dy

    #  get end
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
    cv2.line(img, (far_x, far_y),(base_x, base_y), (255, 0, 0), 2)

    # plot daphnia Length on image (from eye to base)
    cv2.line(img, (cX, cY),(base_x, base_y), (0, 0, 255), 2)

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
    # Load in rayscale, resize
    img = cv2.imread(image)
    # save aspect ratio
    height, width = np.shape(img)[0:2]

    # scale image to 720p width
    scf = 720/width
    nwidth = 720
    nheight = int(height * scf)
    img = cv2.resize(img, (nwidth, nheight))
    
    #grayscale image
    gray = np.uint8(np.mean(img, 2))

    # create uneroded mask
    edges_mag = scharr(gray)
    edges_med = np.median(edges_mag)
    edges_thresh = 2.5*edges_med
    edges = edges_mag >= edges_thresh
    edges = morphology.closing(edges, morphology.square(3))
    edges = ndimage.binary_fill_holes(edges)
    edges = morphology.erosion(edges, morphology.square(3))


    # label imageregions and calculate properties
    label_img = morphology.label(edges, connectivity=2, background=0)
    props = measure.regionprops(label_img, gray)
    props = sorted(props, reverse=True, key=lambda k: k.area)

    # define uneroded binary image
    bw_img = 0*edges
    bw_img = (label_img) == props[0].label
    bw_img_all = bw_img.copy()
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    binary1 = np.uint8(255*bw_img_all)

    # # erode the mask
    # reformat edges to work with opencv
    edges = np.uint8(edges)
    edges_res = edges
    kernel_size = 2
    # continue opening until solidity fits
    while props[0].solidity < 0.93:
        edges_res = edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size,kernel_size))
        edges_res = cv2.morphologyEx(edges_res, cv2.MORPH_OPEN, kernel, iterations = 1)

        # label imageregions and calculate properties
        label_img = morphology.label(edges_res, connectivity=2, background=0)
        props = measure.regionprops(label_img, gray)
        props = sorted(props, reverse=True, key=lambda k: k.area)
        kernel_size += 1

    # get binary image of eroded mask
    bw_img = 0*edges_res
    bw_img = (label_img) == props[0].label
    bw_img_all = bw_img.copy()
    bw_img_all = bw_img_all + ((label_img) == props[0].label)
    binary2 = np.uint8(255*bw_img_all)

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

    # extract daphnia and place on white background
    mask_inv = cv2.bitwise_not(binary2)
    foreground = cv2.bitwise_and(img, img, mask = binary2)
    background = np.copy(img)
    background[:] = 255
    background = cv2.bitwise_and(background, background, mask = mask_inv)
    product = cv2.add(foreground, background)


    # # filter by black color
    full_black = np.array([0, 0, 0])
    half_black = np.array([100, 100, 100])

    # filter with broad spectrum
    black = cv2.inRange(product, full_black, half_black)
    eye_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(2), int(2)))
    black_eroded = cv2.morphologyEx(black, cv2.MORPH_OPEN, eye_kernel, iterations = 2)

    # define contour
    contours, hierarchy = cv2.findContours(copy.deepcopy(black_eroded), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # change thin colour spectrum until contours are of length one
    while len(contours) > 1:
        half_black = half_black - [10, 10, 10]
        black = cv2.inRange(product, full_black, half_black)
        eye_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(2), int(2)))
        black_eroded = cv2.morphologyEx(black, cv2.MORPH_OPEN, eye_kernel, iterations = 2)

        # define contour
        contours, hierarchy = cv2.findContours(copy.deepcopy(black_eroded), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)


    M = cv2.moments(contours[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])


    # # #  find tip of the tail
    # find extreme points on uneroded mask
    contours, hierarchy = cv2.findContours(copy.deepcopy(binary1), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    cnt = contours[0]

    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

    extremes = [leftmost, rightmost, topmost, bottommost]
    # save extremes and eye in a list
    points = extremes + [(cX, cY)]
    # compute distances from eye
    lengths = []
    dxs = []
    dys = []
    for i in range(len(points)):
            dy = points[i][0]-points[4][0]
            dys.append(dy)
            dx = points[i][1]-points[4][1]
            dxs.append(dx)
            L = math.sqrt(dx**2 + dy**2)
            lengths.append(L)


    # find index of max distance
    max_dist_index = lengths.index(max(lengths))

    # get tip of the tail(note that y,x is exchanged)
    far_x = int(cX+dys[max_dist_index])
    far_y = int(cY+dxs[max_dist_index])

    # define distance from eye to tip of tail
    daphnia_Length_eye_tip = max(lengths)

    # # find closest point of mask contour to tip of the tail (base of tail)

    # get contour of eroded mask
    contours, hierarchy = cv2.findContours(copy.deepcopy(binary2), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    # convert contours to a list
    contours = contours[0]

    # convert tail tip to list
    tail_tip = [far_x, far_y]



    lin_distances = np.empty(0)
    for i in range(0,len(contours)):
        con_x = contours[i][0][0]
        con_y = contours[i][0][1]
        lin_dis = math.sqrt(abs(con_x-tail_tip[0])**2 + abs(con_y-tail_tip[1])**2)
        lin_distances = np.append(lin_distances, lin_dis)

    # find index of minimal value
    base_index = np.where(lin_distances == np.min(lin_distances))[0][0]
    # find base
    base = contours[base_index]
    base_x = base[0][0]
    base_y = base[0][1]

    # define tail length
    tail_Length = np.min(lin_distances)
    

    # define Length of daphnia from eye to base of the tail
    daphnia_Length = math.sqrt((cX - base_x)**2 + (cY - base_y)**2)

    # find angle between tail and line from eye to base of tail
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cos_angle = (tail_Length**2 + daphnia_Length**2 - daphnia_Length_eye_tip**2)/(2*tail_Length*daphnia_Length)
        angle = math.acos(cos_angle) * (180/pi)

    # # #  plot everything
    # plot mask contour on image
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

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
        res2 = eye_method(sys.argv[1])
        res3 = eye_method_2(sys.argv[1])
        cv2.imshow('eye method 1', res2['image'])
        cv2.imshow('eye method 2', res3['image'])
    except:
        print('Eye detetion failed!')
    cv2.imshow('head method', res1['image'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
