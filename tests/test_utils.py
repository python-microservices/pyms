"""Test common rest operations wrapper.
"""
import os
import unittest

import pytest

from pyms.exceptions import PackageNotExists
from pyms.utils import check_package_exists, import_package


class ConfUtils(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_check_package_exists_exception(self):
        with pytest.raises(PackageNotExists) as excinfo:
            check_package_exists("this-package-not-exists")
        assert "this-package-not-exists is not installed. try with pip install -U this-package-not-exists" \
               in str(excinfo.value)

    def test_import_package(self):
        os_import = import_package("os")
        assert os_import == os
