import helpers

def test_is_dir():
    # set wrong path
    path_wro = "./images/test_imagessss"

    # test correcwrong path
    with pytest.raises(ArgumentTypeError):
        helpers.is_dir(path_cor)
