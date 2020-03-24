"""Test common rest operations wrapper.
"""
import os
import unittest
from unittest.mock import patch

import pytest

from pyms.cmd import Command
from pyms.exceptions import FileDoesNotExistException, PackageNotExists
from pyms.crypt.fernet import Crypt


class TestCmd(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_crypt_file_error(self):
        arguments = ["encrypt", "prueba"]
        cmd = Command(arguments=arguments, autorun=False)
        with pytest.raises(FileDoesNotExistException) as excinfo:
            cmd.run()
        assert ("Decrypt key None not exists. You must set a correct env var KEY_FILE or run "
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

    @patch('pyms.cmd.main.Command.get_input', return_value='n')
    def test_output_key(self, input):
        crypt = Crypt()
        arguments = ["create-key", ]
        cmd = Command(arguments=arguments, autorun=False)
        cmd.run()
        with pytest.raises(FileNotFoundError) as excinfo:
            crypt.delete_key()
        assert "[Errno 2] No such file or directory: 'key.key'" in str(excinfo.value)

    def test_startproject_error(self):
        arguments = ["startproject"]
        cmd = Command(arguments=arguments, autorun=False)
        with pytest.raises(PackageNotExists) as excinfo:
            cmd.run()
        assert "cookiecutter is not installed. try with pip install -U cookiecutter" in str(excinfo.value)
