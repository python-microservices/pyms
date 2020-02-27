"""Test common rest operations wrapper.
"""
import os
import unittest

import pytest

from pyms.exceptions import PackageNotExists, FileDoesNotExistException
from pyms.utils import check_package_exists, import_package
from pyms.utils.crypt import Crypt


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


class CryptUtils(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_crypt_file_error(self):
        crypt = Crypt()
        with pytest.raises(FileDoesNotExistException) as excinfo:
            crypt.read_key()
        assert ("Decrypt key None not exists. You must set a correct env var KEY_FILE or run "
                "`pyms crypt create-key` command") \
               in str(excinfo.value)

    def test_crypt_file_ok(self):
        crypt = Crypt()
        crypt.generate_key("mypassword", True)
        message = "My crypt message"
        encrypt_message = crypt.encrypt(message)
        assert message == crypt.decrypt(str(encrypt_message, encoding="utf-8"))
        crypt.delete_key()
