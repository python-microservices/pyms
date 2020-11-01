"""Test common rest operations wrapper.
"""
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import pytest
from prance.util.url import ResolutionError
from pyms.cmd import Command
from pyms.exceptions import FileDoesNotExistException, PackageNotExists
from pyms.crypt.fernet import Crypt
from pyms.flask.services.swagger import get_bundled_specs
from tests.common import remove_conf_file


class TestCmd(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_crypt_file_error(self):
        arguments = ["encrypt", "prueba"]
        cmd = Command(arguments=arguments, autorun=False)
        with pytest.raises(FileDoesNotExistException) as excinfo:
            cmd.run()
        assert ("Decrypt key None not exists. You must set a correct env var PYMS_KEY_FILE or run "
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

    def test_get_bundled_specs(self):
        specs = get_bundled_specs(Path("tests/swagger_for_tests/swagger.yaml"))
        self.assertEqual(specs.get('swagger'), "2.0")
        self.assertEqual(specs.get('info').get('version'), "1.0.0")
        self.assertEqual(specs.get('info').get('contact').get('email'), "apiteam@swagger.io")

    def test_merge_swagger_ok(self):
        arguments = ["merge-swagger", "--file", "tests/swagger_for_tests/swagger.yaml", ]
        cmd = Command(arguments=arguments, autorun=False)
        assert cmd.run()
        os.remove("tests/swagger_for_tests/swagger-complete.yaml")

    def test_merge_swagger_error(self):
        arguments = ["merge-swagger", ]
        cmd = Command(arguments=arguments, autorun=False)
        with pytest.raises(ResolutionError) as excinfo:
            cmd.run()

    @patch('pyms.cmd.main.Command.yes_no_input', return_value=True)
    def test_create_config_all(self, input):
        # Remove config file if already exists for test
        remove_conf_file()
        arguments = ["create-config"]
        cmd = Command(arguments=arguments, autorun=False)
        assert cmd.run()
        assert not cmd.run()
        remove_conf_file()
