import helpers
import pytest

# test is_dir function
def test_is_dir():
    # set wrong path
    path_wro = "./images/test_imagessss"

    # test correcwrong path
    with pytest.raises(Exception):
        helpers.is_dir(path_cor)

# test check scale function
def test_check_scale():
    # set path to wrong scale
    pth = "./images/test_images_scale_wrong"
    
    # expect error
    with pytest.raises(ValueError):
        helpers.check_scale(pth)