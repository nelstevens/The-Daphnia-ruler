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
def create_props(edges, gray, eyeMethod=False):
    '''
    labels image and defines properties
    '''
    # label imageregions and calculate properties
    label_img = morphology.label(edges, connectivity=2, background=0)
    props = measure.regionprops(label_img, gray)
    props = sorted(props, reverse=True, key=lambda k: k.area)

    # return properties only props if eyemethod = F else props and label_img
    if eyeMethod == False:
        return(props)
    else:
        return([props, label_img])

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

# create function to plot contour on image
def plt_contour(binaryimg, img):
    '''
    plots contour on image
    '''
    # get contours
    contours, hierarchy = cv2.findContours(binaryimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw contour on image
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
    # return image
    return(img)

# create function to plot elipse on image
def plt_elipse(img, props):
    '''
    plots elipse on image
    '''
    # plot elipse on image
    cv2.ellipse(img, (int(props[0].centroid[1]), int(props[0].centroid[0])),
                (int(props[0].major_axis_length/2), int(props[0].minor_axis_length/2)),
                (-props[0].orientation*180/pi+90), 0, 360, 0, 0)
    # return img
    return(img)

# create function to plot major axis on image
def plt_majaxis(img, props):
    '''
    plots major axis on image
    '''
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

    # return image
    return(img)

# create function to plot minor axis on image
def plt_minaxis(img, props):
    '''
    plots minro axis on image
    '''
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

    # return image
    return(img)

# create function to make dictionary of results
def make_res(img, props, scf, image):
    '''
    creates dictionary with results
    '''
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

    # return dictionary
    return(res)

# create function to find eye in binary image
def find_eye(binary2, img):
    '''
    find position of the eye and teturns its x,y values
    '''
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
    # return eye position
    return([cX, cY])
# create funtion to find tip of tail and define distance from eye to tip of tail
def find_tip(binary1, cX, cY):
    '''
    find position of tip of tail and length between eye and tip of tail.
    '''
    # define contours
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

    # return postion and length
    return([far_x, far_y, daphnia_Length_eye_tip])