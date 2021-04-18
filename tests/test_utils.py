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