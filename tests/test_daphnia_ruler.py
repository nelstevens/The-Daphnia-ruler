# test daphnia ruler
import sys
import daphnia_ruler as dr
import os
import pytest
# create directory paths
pths = [os.path.join(os.getcwd(), "tests", "test_dirs", "test_ruler"), os.path.join(os.getcwd(), "tests", "test_dirs", "test_ruler_recursive")]

# test main without other options
@pytest.mark.parametrize("dirs", pths)
def test_main(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with eye method enabled
@pytest.mark.parametrize("dirs", pths)
def test_main_eye(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-e", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with eye method and scale enabled
@pytest.mark.parametrize("dirs", pths)
def test_main_eye_scale(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-e", "-s", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with eye method, scale and no images enabled
@pytest.mark.parametrize("dirs", pths)
def test_main_eye_scale_no(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-e", "-s", "-n", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with scale enabled only
@pytest.mark.parametrize("dirs", pths)
def test_main_scale(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-s", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with scale and no images enabled only
@pytest.mark.parametrize("dirs", pths)
def test_main_scale_no(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-s", "-n", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with scale and no images enabled only
@pytest.mark.parametrize("dirs", pths)
def test_main_no(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-n", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False

# test main with scale and no images enabled only
@pytest.mark.parametrize("dirs", pths)
def test_main_eye_no(monkeypatch, dirs):
    # set sys.argv correctly
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["daphnia_ruler.py", "-e", "-n", "-p", dirs])

        # assert no error
        try:
            dr.main()
            assert True
        except Exception:
            assert False