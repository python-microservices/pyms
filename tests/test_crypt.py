import logging
import os
import unittest

import pytest

from pyms.config import get_conf
from pyms.constants import LOGGER_NAME, CONFIGMAP_FILE_ENVIRONMENT, CRYPT_FILE_KEY_ENVIRONMENT, CONFIG_BASE
from pyms.crypt.driver import CryptAbstract
from pyms.crypt.fernet import Crypt
from pyms.exceptions import FileDoesNotExistException
from tests.common import MyMicroserviceNoSingleton

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


class CryptFernet(unittest.TestCase):
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


class GetConfigEncrypted(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-encrypted.yml")
        os.environ[CRYPT_FILE_KEY_ENVIRONMENT] = os.path.join(self.BASE_DIR, "key.key")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]
        del os.environ[CRYPT_FILE_KEY_ENVIRONMENT]

    def test_encrypt_conf(self):
        crypt = Crypt(path=self.BASE_DIR)
        crypt._loader.put_file(b"9IXx2F5d5Ob-h5xdCnFSUXhuFKLGRibvLfSbixpcfCw=", "wb")
        config = get_conf(service=CONFIG_BASE, uppercase=True, crypt=Crypt)
        crypt.delete_key()
        assert config.database_url == "http://database-url"


class FlaskWithEncryptedFernetTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests-flask-encrypted-fernet.yml")
        os.environ[CRYPT_FILE_KEY_ENVIRONMENT] = os.path.join(self.BASE_DIR, "key.key")
        self.crypt = Crypt(path=self.BASE_DIR)
        self.crypt._loader.put_file(b"9IXx2F5d5Ob-h5xdCnFSUXhuFKLGRibvLfSbixpcfCw=", "wb")
        ms = MyMicroserviceNoSingleton(path=__file__)
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice With Flask encrypted", self.app.config["APP_NAME"])

    def tearDown(self):
        self.crypt.delete_key()
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]
        del os.environ[CRYPT_FILE_KEY_ENVIRONMENT]

    def test_fask_fernet(self):
        assert self.app.ms.config.database_url == "http://database-url"
        assert self.app.config["DATABASE_URL"] == "http://database-url"

    def test_fask_fernet_sqlalchemy(self):
        assert self.app.ms.config.SQLALCHEMY_DATABASE_URI == "http://database-url"
        assert self.app.config["SQLALCHEMY_DATABASE_URI"] == "http://database-url"


class FlaskWithEncryptedNoneTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests-flask-encrypted-none.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice With Flask encrypted None", self.app.config["APP_NAME"])

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_fask_none(self):
        assert self.app.ms.config.database_url == "http://database-url"
        assert self.app.config["DATABASE_URL"] == "http://database-url"

    def test_fask_none_sqlalchemy(self):
        assert self.app.ms.config.SQLALCHEMY_DATABASE_URI == "http://database-url"
        assert self.app.config["SQLALCHEMY_DATABASE_URI"] == "http://database-url"
