import os
import utils
import numpy as np

# test importing, resizing and grayscaling image
def test_import_image():
    # run funtion to create dictionary
    res = utils.import_image("./images/test_images/sample1.JPG")

    # load comparison files
    img_ar = np.load("./tests/assert_img_sample1.npy")
    gray_ar = np.load("./tests/assert_gray_sample1.npy")

    # compare both image arrays
    comparison = img_ar == res["img"]
    eq = comparison.all()

    comparison_g = gray_ar == res["gray"]
    eq_g = comparison_g.all()

    # assert true
    assert eq == True
    assert eq_g == True

    # assert correct scaling factor
    assert res["scf"] == 0.375
    
# test creating mask
def test_create_mask():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # load comparison file
    edges_ar = np.load("./tests/assert_edges_sample1.npy")

    # compare array
    comparison = edges == edges_ar
    eq = comparison.all()

    # assert True
    assert eq == True

# test creating properties
def test_create_props():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # assert almost equal with numpy
    np.testing.assert_almost_equal(props[0].solidity, 0.685, 3)
    # add eyeMethod options here!
    
# test eroding mask
def test_erode_mask():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # assert correct solidity
    assert props[0].solidity >= 0.93

# test plotting binary image
def test_plt_binary():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # load comparison array
    bin2 = np.load("./tests/assert_binary_sample1.npy")

    # compare array
    comparison = binary2 == bin2
    eq = comparison.all()

    # assert equality
    assert eq == True

# test plotting contour
def test_plt_contour():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # define img
    img = res["img"]

    # run plotting contour
    img = utils.plt_contour(binary2, img)

    # load assertion array
    image = np.load("./tests/assert_contour_sample1.npy")

    # compare arrays
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True

# test plotting elipse
def test_plt_elipse():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # define img
    img = res["img"]

    # run plotting contour
    img = utils.plt_contour(binary2, img)

    # run plotting elipse
    img = utils.plt_elipse(img, props)

    # load comparison array
    image = np.load("./tests/assert_elipse_sample1.npy")

    # compare array
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True

# test plotting major axis
def test_plt_majaxis():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # define img
    img = res["img"]

    # run plotting contour
    img = utils.plt_contour(binary2, img)

    # run plotting elipse
    img = utils.plt_elipse(img, props)

    # run plotting major axis
    img = utils.plt_majaxis(img, props)

    # import comparison array
    image = np.load("./tests/assert_majaxis_sample1.npy")

    # compare array
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True

# test ploting minor axis
def test_plt_minaxis():
     # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # define img
    img = res["img"]

    # run plotting contour
    img = utils.plt_contour(binary2, img)

    # run plotting elipse
    img = utils.plt_elipse(img, props)

    # run plotting major axis
    img = utils.plt_majaxis(img, props)

    # run ploting minor axis
    img = utils.plt_minaxis(img, props)

    # import comparison array
    image = np.load("./tests/assert_minaxis_sample1.npy")

    # compare arrays
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True

# test returning results
def test_make_res():
    # load image
    res = utils.import_image("./images/test_images/sample1.JPG")

    # run edges function
    edges = utils.create_mask(res["gray"])

    # run make properties
    props = utils.create_props(edges, res["gray"])

    # define gray
    gray = res["gray"]

    # run erode mask
    props, edges_res, label_img = utils.erode_mask(edges, props, gray)

    # run ploting binary image
    binary2 = utils.plt_binary(edges_res, label_img, props)

    # define img
    img = res["img"]

    # run plotting contour
    img = utils.plt_contour(binary2, img)

    # run plotting elipse
    img = utils.plt_elipse(img, props)

    # run plotting major axis
    img = utils.plt_majaxis(img, props)

    # run ploting minor axis
    img = utils.plt_minaxis(img, props)

    # define image path
    image = os.path.join(os.getcwd(), "images", "test_images", "sample1.JPG")
    # define scaling factor
    scf = res["scf"]

    # run returning results
    res = utils.make_res(img, props, scf, image)

    # load comparison array
    compimg = np.load("./tests/assert_minaxis_sample1.npy")

    # assert img array equality
    comparison = img == compimg
    eq = comparison.all()
    assert eq == True

    # assert correct ID
    assert res["ID"] == "test_images/sample1.JPG"

    # assert perimeter
    np.testing.assert_almost_equal(res["perimeter"], 1038.1889, 4)

    # assert area
    np.testing.assert_almost_equal(res["area"], 65656.8888, 4)

    # assert minor axis
    np.testing.assert_almost_equal(res["minor"], 207.7906, 4)

    # assert solidity
    np.testing.assert_almost_equal(res["solidity"], 0.9870, 4)

    # assert major axis
    np.testing.assert_almost_equal(res["full.Length"], 406.9932, 4)

# test finding the eye
def test_find_eye():
    # import and resize
    img_res = utils.import_image("./images/test_images/sample1.JPG")

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

    # assert correct cX and cY
    assert cX == 342
    assert cY == 210
# test_find_tip
def test_find_tip():
    # import and resize
    img_res = utils.import_image("./images/test_images/sample1.JPG")

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

    # assert correct values for far_y, far_y and daphnia_Length_eye_tip
    assert far_x == 435
    assert far_y == 361
    np.testing.assert_almost_equal(daphnia_Length_eye_tip, 177.3415, 4)

# test find_base
def test_find_base():
    # import and resize
    img_res = utils.import_image("./images/test_images/sample1.JPG")

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

    # assert correct values
    assert base_x == 401
    assert base_y == 329
    np.testing.assert_almost_equal(daphnia_Length, 132.8232, 4)
    np.testing.assert_almost_equal(angle, 159.6364, 4)
    np.testing.assert_almost_equal(tail_Length, 46.6905, 4)

# test plt_tail
def test_plt_tail():
    # import and resize
    img_res = utils.import_image("./images/test_images/sample1.JPG")

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

    # plot tail on image
    img = utils.plt_tail(img, far_x, far_y, base_x, base_y)

    # import comparison array
    image = np.load("./tests/assert_tail_sample1.npy")

    # compare arrays
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True
# test plt_length
def test_plt_length():
    # import and resize
    img_res = utils.import_image("./images/test_images/sample1.JPG")

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

    # plot daphnia Length on image (from eye to base)
    img = utils. plt_length(img, cX, cY, base_x, base_y)

    # import comparison array
    image = np.load("./tests/assert_lengtheb_sample1.npy")

    # compare arrays
    comparison = img == image
    eq = comparison.all()

    # assert equality
    assert eq == True