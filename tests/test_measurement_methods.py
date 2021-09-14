import measurement_methods
import numpy as np
import os

# test head method
def test_head_method():
    pth = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample1.JPG")
    res = measurement_methods.head_method(pth)

    # assert dictionary contents one by one
    # load comparison array
    compimg = np.load("./tests/test_arrays/assert_minaxis_sample1.npy")

    # assert img array equality
    comparison = res["image"] == compimg
    eq = comparison.all()
    assert eq == True

    # assert correct ID
    assert res["ID"] == "test_images/sample1.JPG" or res["ID"] == "test_images\\sample1.JPG"

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

# test eye method
def test_eye_method2():
    pth = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample1.JPG")
    res = measurement_methods.eye_method_2(pth)

    # assert dictionary one by one
        # assert correct ID
    assert res["ID"] == "test_images/sample1.JPG" or res["ID"] == "test_images\\sample1.JPG"

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

    # add eye_method specific measurements!