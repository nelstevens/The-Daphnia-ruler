# test daphnia ruler
import sys
import daphnia_ruler as dr
import os
import pytest
# create directory paths
pths = [os.path.join(os.getcwd(), "tests", "test_dirs", "test_ruler"), os.path.join(os.getcwd(), "tests", "test_dirs", "test_ruler_recursive")]
# test main
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