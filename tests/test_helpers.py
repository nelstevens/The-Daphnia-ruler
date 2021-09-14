import helpers
import pytest

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