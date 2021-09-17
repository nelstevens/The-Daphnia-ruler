import helpers
import pytest

# test if measure_except_eye behaves properly on different images
def test_measure_except_eye():
    # path to image where eye can be detected
    pth_ey = "./tests/test_dirs/test_images/sample1.JPG"
    # path to image where eye can't be detected
    pth_no = "./tests/test_dirs/test_images/sample3.JPG"

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
    pth_ey = "./tests/test_dirs/test_images/sample1.JPG"
    # path to image where eye can't be detected
    pth_no = "./tests/test_dirs/test_images/sample3.JPG"

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