import base64
import os
from typing import Text

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pyms.constants import CRYPT_FILE_KEY_ENVIRONMENT, DEFAULT_KEY_FILENAME, CRYPT_FILE_KEY_ENVIRONMENT_LEGACY
from pyms.crypt.driver import CryptAbstract
from pyms.exceptions import FileDoesNotExistException
from pyms.utils.files import LoadFile


class Crypt(CryptAbstract):
    def __init__(self, *args, **kwargs):
        # TODO Remove temporally backward compatibility on future versions
        crypt_file_key_env = self.__get_updated_crypt_file_key_env()  # Temporally backward compatibility
        self._loader = LoadFile(kwargs.get("path"), crypt_file_key_env, DEFAULT_KEY_FILENAME)
        super().__init__(*args, **kwargs)

    def generate_key(self, password: Text, write_to_file: bool = False) -> bytes:
        byte_password = password.encode()  # Convert to type bytes
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512_256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(byte_password))  # Can only use kdf once
        if write_to_file:
            self._loader.put_file(key, 'wb')
        return key

    def read_key(self):
        key = self._loader.get_file()
        if not key:
            # TODO Remove temporally backward compatibility on future versions
            crypt_file_key_env = self.__get_updated_crypt_file_key_env()  # Temporally backward compatibility
            raise FileDoesNotExistException(
                "Decrypt key {} not exists. You must set a correct env var {} "
                "or run `pyms crypt create-key` command".format(self._loader.path, crypt_file_key_env))
        return key

    def encrypt(self, message):
        key = self.read_key()
        message = message.encode()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return encrypted

    def decrypt(self, encrypted):
        key = self.read_key()
        encrypted = encrypted.encode()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        return str(decrypted, encoding="utf-8")

    def delete_key(self):
        os.remove(self._loader.get_path_from_env())

    @staticmethod
    def __get_updated_crypt_file_key_env() -> str:
        result = CRYPT_FILE_KEY_ENVIRONMENT
        if (os.getenv(CRYPT_FILE_KEY_ENVIRONMENT_LEGACY) is not None) and (os.getenv(CRYPT_FILE_KEY_ENVIRONMENT) is None):
            result = CRYPT_FILE_KEY_ENVIRONMENT_LEGACY
        return result
