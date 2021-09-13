import measurement_methods
import numpy as np

# test head method
def test_head_method():
    res = measurement_methods.head_method("./images/test_images/sample1.JPG")

    # assert dictionary contents one by one
    # load comparison array
    compimg = np.load("./tests/assert_minaxis_sample1.npy")

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
    res = measurement_methods.eye_method_2("./images/test_images/sample1.JPG")

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