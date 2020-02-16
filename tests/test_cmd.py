"""Test common rest operations wrapper.
"""
import os
import unittest
from unittest.mock import patch

import pytest

from pyms.cmd import Command
from pyms.exceptions import FileDoesNotExistException
from pyms.utils.crypt import Crypt


class TestCmd(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_crypt_file_error(self):
        arguments = ["encrypt", "prueba"]
        cmd = Command(arguments=arguments, autorun=False)
        with pytest.raises(FileDoesNotExistException) as excinfo:
            cmd.run()
        assert ("Decrypt key key.key not exists. You must set a correct env var KEY_FILE or run "
                "`pyms crypt create-key` command") \
               in str(excinfo.value)

    def test_crypt_file_ok(self):
        crypt = Crypt()
        crypt.generate_key("mypassword", True)
        arguments = ["encrypt", "prueba"]
        cmd = Command(arguments=arguments, autorun=False)
        cmd.run()
        crypt.delete_key()

    @patch('pyms.cmd.main.Command.get_input', return_value='Y')
    def test_generate_file_ok(self, input):
        crypt = Crypt()
        arguments = ["create-key", ]
        cmd = Command(arguments=arguments, autorun=False)
        cmd.run()
        crypt.delete_key()
