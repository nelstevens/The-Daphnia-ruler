import helpers
import pytest
import os
import numpy as np
import sys
import daphnia_ruler as dr

# test if measure_except_eye behaves properly on different images
def test_measure_except_eye():
    # path to image where eye can be detected
    pth_ey = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample1.JPG")
    # path to image where eye can't be detected
    pth_no = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample3.JPG")

    # run measure_except_eye on both
    res_eye = helpers.measure_except_eye(pth_ey)
    res_no = helpers.measure_except_eye(pth_no)

    # assert that res_eye[eye.Length] exists
    assert "eye.Length" in res_eye.keys()
    # assert that res_no[eye.Length] does not exist
    assert "eye.Length" not in res_no.keys()

# test that measure_except never returns eye.Length
def test_measure_except():
    # path to image where eye can be detected
    pth_ey = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample1.JPG")
    # path to image where eye can't be detected
    pth_no = os.path.join(os.getcwd(), "tests", "test_dirs", "test_images", "sample3.JPG")

    # run measure_except_eye on both
    res_eye = helpers.measure_except(pth_ey)
    res_no = helpers.measure_except(pth_no)

    # assert that res_eye[eye.Length] does not exists
    assert "eye.Length" not in res_eye.keys()
    # assert that res_no[eye.Length] does not exist
    assert "eye.Length" not in res_no.keys()

# test is_dir function
def test_is_dir():
    # set wrong path
    path_wro = "./tests/test_dirs/test_imagessss"

    # test correcwrong path
    with pytest.raises(Exception):
        helpers.is_dir(path_wro)

# test check scale function
def test_check_scale():
    # set path to wrong scale
    pth = "./tests/test_dirs/test_images_scale_wrong"
    
    # expect error
    with pytest.raises(ValueError):
        helpers.check_scale(pth)
    
    # excpect error also when wrong scale in higher level directory
    pth = "./tests/test_dirs/test_images_2ndlvl_scale_wrong"

    # expect error
    with pytest.raises(ValueError):
        helpers.check_scale(pth)

# test scale measurement function
def test_scale_measurements_eye(monkeypatch):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-p", "./tests/test_dirs/test_images", "-s", "-e"])
        # load input array
        inarr = np.load(os.path.join(os.getcwd(), "tests", "test_arrays", "scale_measurement_array.npy"), allow_pickle = True)
        actual = helpers.scale_measurements(
            res = inarr, 
            img_dir = ".",
            sc_factor = 0.032,
            args = dr.parse_args(sys.argv)
        )
        # load expected
        expected = np.load(os.path.join(os.getcwd(), "tests", "test_arrays", "expected_scale_measurement_array.npy"), allow_pickle = True)

        # assert correct for length in sample1
        assert actual[0]["eye.Length"] == expected[0]["eye.Length"]
        # assert exception for eye length in sample 3
        with pytest.raises(KeyError):
            assert actual[1]["eye.Length"] == expected[1]["eye.Length"]
        # assert correct for tail length in sample1
        assert actual[0]["tail.Length"] == expected[0]["tail.Length"]
        # assert exception for eye length in sample 3
        with pytest.raises(KeyError):
            assert actual[1]["tail.Length"] == expected[1]["tail.Length"]
        
        # assert correctness of rest
        for key in ["perimeter", "area", "minor", "full.Length"]:
            assert actual[0][key] == expected[0][key]
            assert actual[1][key] == expected[1][key]

# test scale measurement function withou eye method
def test_scale_measurements_head(monkeypatch):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-p", "./tests/test_dirs/test_images", "-s"])
        # load input array
        inarr = np.load(os.path.join(os.getcwd(), "tests", "test_arrays", "scale_measurement_array.npy"), allow_pickle = True)
        actual = helpers.scale_measurements(
            res = inarr, 
            img_dir = ".",
            sc_factor = 0.032,
            args = dr.parse_args(sys.argv)
        )
        # load expected
        expected = np.load(os.path.join(os.getcwd(), "tests", "test_arrays", "expected_scale_measurement_array.npy"), allow_pickle = True)
        
        # assert correctness of rest
        for key in ["perimeter", "area", "minor", "full.Length"]:
            assert actual[0][key] == expected[0][key]
            assert actual[1][key] == expected[1][key]
