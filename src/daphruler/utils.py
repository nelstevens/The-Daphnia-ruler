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
    """imports, resizes and grayscales image.
     returns additional info on image.

    Parameters
    ----------
    image : str
        path to image source
        

    Returns
    -------
    dictionary containing. image as numpy array, grayscale image as numpy array, scaling factor as float
    """
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
    """masks grayscaled image

    Parameters
    ----------
    gray :  numpy array
        grayscaled image array
        

    Returns
    -------
    array of image with edges highlighted
    """
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
    """labels image and defines properties

    Parameters
    ----------
    edges : array
        array of image with edges highlighted
        
    gray : array
        grascaled image array
        
    eyeMethod : bool
        whether to use eyeMethod
         (Default value = False)

    Returns
    -------
    image properties
    """
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
    """erodes edges to discard appendages

    Parameters
    ----------
    edges : array
        array with edges highlighted
        
    props : image properties
        
    gray : array
        grayscaled image array
        

    Returns
    -------
    list with new properties, new edges and labeled image
    """
    # reformat edges to work with opencv
    edges = np.uint8(edges)
    # copy edges in case no opening is necessary
    edges_res = edges
    kernel_size = 2
    # create labeled image in case no opening is necessary
    label_img = morphology.label(edges, connectivity=2, background=0)
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
    """creates binary image in numpy format

    Parameters
    ----------
    edges_res : array
        array with edges highlighted
        
    label_img : labeled images
        
    props : image properties
        

    Returns
    -------
    binary numpy array
    """
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
    """plots contour on image

    Parameters
    ----------
    binaryimg : array
        binary image array
        
    img : array
        imagearray
        

    Returns
    -------
    image array with contour highlighted
    """
    # get contours
    contours, hierarchy = cv2.findContours(binaryimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw contour on image
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
    # return image
    return(img)

# create function to plot elipse on image
def plt_elipse(img, props):
    """plots elipse on image

    Parameters
    ----------
    img : array
        image array
        
    props : image properties
        

    Returns
    -------
    image array with elipse highlighted
    """
    # plot elipse on image
    cv2.ellipse(img, (int(props[0].centroid[1]), int(props[0].centroid[0])),
                (int(props[0].major_axis_length/2), int(props[0].minor_axis_length/2)),
                (-props[0].orientation*180/pi+90), 0, 360, 0, 0)
    # return img
    return(img)

# create function to plot major axis on image
def plt_majaxis(img, props):
    """plots major axis on image

    Parameters
    ----------
    img : array
        image array
        
    props : image properties
        

    Returns
    -------
    image array with major axis highlighted
    """
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
    """plots minro axis on image

    Parameters
    ----------
    img :array
        image array
        
    props : image properties
        

    Returns
    -------
    image array with minor axis highlighted
    """
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
def make_res(img, props, scf, image, eyeMethod = False, tail_Length = None, daphnia_Length = None, angle = None):
    """creates dictionary with results

    Parameters
    ----------
    img : array
        image array
        
    props : image properties
        
    scf : float
        scaling factor
        
    image : str
        path to image source
        
    eyeMethod : bool
        whether to use eyemethod
         (Default value = False)
    tail_Length : float
        Length of tail
         (Default value = None)
    daphnia_Length : float
        Length of daphnia
         (Default value = None)
    angle :
        Angle between tail and major axis
         (Default value = None)

    Returns
    -------
    dictionary with measurement results.
    """
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

        # add additions if eyeMethod is true
    if eyeMethod:
        tail_Length = tail_Length/scf
        daphnia_Length = daphnia_Length/scf
        res['tail.Length'] = tail_Length
        res['eye.Length'] = daphnia_Length
        res['tail.angle'] = angle

    # return dictionary
    return(res)

# create function to find eye in binary image
def find_eye(binary2, img):
    """find position of the eye and teturns its x,y values

    Parameters
    ----------
    binary2 : array
        binary array
        
    img : array
        image array
        

    Returns
    -------
    coordinated of eye as list
    """
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
    """find position of tip of tail and length between eye and tip of tail.

    Parameters
    ----------
    binary1 : array
        binary image array
        
    cX : int
        x coordinate of eye
        
    cY : int
        y coordinate of eye
        

    Returns
    -------
    coordinates of tail tip and distance between eye and tip as list.
    """
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

# create function to find base of tail
def find_base(binary2, far_x, far_y, cX, cY, daphnia_Length_eye_tip):
    """finds base of tail.

    Parameters
    ----------
    binary2 : array
        binary image array
        
    far_x : int
        x coordinate of tail tip
        
    far_y : inst
        x coordinate of tail tip
        
    cX : int
        x coordinate of eye
        
    cY : inst
        y coordinate of eye
        
    daphnia_Length_eye_tip : float
        distance between eye and tail tip
        

    Returns
    -------
    list
    """
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

    # return list
    return([base_x, base_y, daphnia_Length, angle, contours, tail_Length])

# define function to plot tail on image
def plt_tail(img, far_x, far_y, base_x, base_y):
    """plots tail on image.

    Parameters
    ----------
    img : array
        image array
        
    far_x : int
        x coordinate of tail tip
        
    far_y : int
        y coordinate of tail tip
        
    base_x : int
        x coordinate of tail base
        
    base_y : int
        y coordinate of tail base
        

    Returns
    -------
    image array with tail tip highlighted
    """
    # plot tail on image
    cv2.line(img, (far_x,far_y),(base_x, base_y), (255, 0, 0), 2)

    # return image
    return(img)

# define function to plot distance of eye to base of tail
def plt_length(img, cX, cY, base_x, base_y):
    """plots length of daphnia on image (length = line between eye and base of tail)

    Parameters
    ----------
    img : array
        image array
        
    cX : int
        x coordinate of eye
        
    cY : int
        y coordinate of eye
        
    base_x : int
        x coordinate of tail base
        
    base_y : int
        y coordinate of tail base
        

    Returns
    -------
    image array with daphnia length highlighted
    """
    # plot daphnia Length on image (from eye to base)
    cv2.line(img, (cX, cY), (base_x, base_y), (0, 0, 255), 2)

    # return image
    return(img)