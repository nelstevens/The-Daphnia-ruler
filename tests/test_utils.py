import os
import utils
import numpy as np

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