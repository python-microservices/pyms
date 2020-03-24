import logging
import unittest

import pytest

from pyms.constants import LOGGER_NAME
from pyms.crypt.driver import CryptAbstract

logger = logging.getLogger(LOGGER_NAME)


class MockDecrypt(CryptAbstract):
    pass


class MockDecrypt2(CryptAbstract):
    def encrypt(self, message):
        return super().encrypt(message)

    def decrypt(self, encrypted):
        return super().encrypt(encrypted)


class CryptTests(unittest.TestCase):

    def test_ko(self):
        with pytest.raises(TypeError) as excinfo:
            MockDecrypt()
        assert "Can't instantiate abstract class MockDecrypt with abstract methods decrypt, encrypt" in str(
            excinfo.value)

    @staticmethod
    def test_ko_encrypt():
        crypt = MockDecrypt2()
        with pytest.raises(NotImplementedError) as excinfo:
            crypt.encrypt("test")
        assert "" == str(excinfo.value)

    @staticmethod
    def test_ko_decrypt():
        crypt = MockDecrypt2()
        with pytest.raises(NotImplementedError) as excinfo:
            crypt.decrypt("test")
        assert "" == str(excinfo.value)
