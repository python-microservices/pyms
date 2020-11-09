#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import argparse
import os
import sys
from distutils.util import strtobool

from pyms.config import create_conf_file
from pyms.crypt.fernet import Crypt
from pyms.flask.services.swagger import merge_swagger_file
from pyms.utils import check_package_exists, import_from, utils


class Command:
    config = None

    parser = None

    args = []

    # flake8: noqa: C901
    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        autorun = kwargs.get("autorun", True)
        if not arguments:  # pragma: no cover
            arguments = sys.argv[1:]

        parser = argparse.ArgumentParser(description="Python Microservices")

        commands = parser.add_subparsers(title="Commands", description="Available commands", dest="command_name")

        parser_encrypt = commands.add_parser("encrypt", help="Encrypt a string")
        parser_encrypt.add_argument("encrypt", default="", type=str, help="Encrypt a string")

        parser_create_key = commands.add_parser("create-key", help="Generate a Key to encrypt strings in config")
        parser_create_key.add_argument(
            "create_key", action="store_true", help="Generate a Key to encrypt strings in config"
        )

        parser_startproject = commands.add_parser(
            "startproject",
            help="Generate a project from https://github.com/python-microservices/microservices-template",
        )
        parser_startproject.add_argument(
            "startproject",
            action="store_true",
            help="Generate a project from https://github.com/python-microservices/microservices-template",
        )

        parser_startproject.add_argument(
            "-b", "--branch", help="Select a branch from https://github.com/python-microservices/microservices-template"
        )

        parser_merge_swagger = commands.add_parser("merge-swagger", help="Merge swagger into a single file")
        parser_merge_swagger.add_argument("merge_swagger", action="store_true", help="Merge swagger into a single file")
        parser_merge_swagger.add_argument(
            "-f", "--file", default=os.path.join("project", "swagger", "swagger.yaml"), help="Swagger file path"
        )

        parser_create_config = commands.add_parser("create-config", help="Generate a config file")
        parser_create_config.add_argument("create_config", action="store_true", help="Generate a config file")

        parser.add_argument("-v", "--verbose", default="", type=str, help="Verbose ")

        args = parser.parse_args(arguments)
        try:
            self.create_key = args.create_key
        except AttributeError:
            self.create_key = False
        try:
            self.encrypt = args.encrypt
        except AttributeError:
            self.encrypt = ""
        try:
            self.startproject = args.startproject
            self.branch = args.branch
        except AttributeError:
            self.startproject = False
        try:
            self.merge_swagger = args.merge_swagger
            self.file = args.file
        except AttributeError:
            self.merge_swagger = False
        try:
            self.create_config = args.create_config
        except Exception:
            self.create_config = False
        self.verbose = len(args.verbose)
        if autorun:  # pragma: no cover
            result = self.run()
            if result:
                self.exit_ok("OK")
            else:
                self.print_error("ERROR")

    @staticmethod
    def get_input(msg):  # pragma: no cover
        return input(msg)  # nosec

    def run(self):
        crypt = Crypt()
        if self.create_key:
            path = crypt._loader.get_path_from_env()  # pylint: disable=protected-access
            pwd = self.get_input("Type a password to generate the key file: ")
            # Should use yes_no_input insted of get input below
            # the result should be validated for Yes (Y|y) rather allowing anything other than 'n'
            generate_file = self.get_input("Do you want to generate a file in {}? [Y/n]".format(path))
            generate_file = generate_file.lower() != "n"
            key = crypt.generate_key(pwd, generate_file)
            if generate_file:
                self.print_ok("File {} generated OK".format(path))
            else:
                self.print_ok("Key generated: {}".format(key))
        if self.encrypt:
            # Spoted Unhandle exceptions - The encrypt function throws FileDoesNotExistException, ValueError
            # which are not currently handled
            encrypted = crypt.encrypt(self.encrypt)
            self.print_ok("Encrypted OK: {}".format(encrypted))
        if self.startproject:
            check_package_exists("cookiecutter")
            cookiecutter = import_from("cookiecutter.main", "cookiecutter")
            cookiecutter("gh:python-microservices/cookiecutter-pyms", checkout=self.branch)
            self.print_ok("Created project OK")
        if self.merge_swagger:
            try:
                merge_swagger_file(main_file=self.file)
                self.print_ok("Swagger file generated [swagger-complete.yaml]")
            except FileNotFoundError as ex:
                self.print_error(ex.__str__())
                return False
        if self.create_config:
            use_requests = self.yes_no_input("Do you want to use request")
            use_swagger = self.yes_no_input("Do you want to use swagger")
            try:
                conf_file_path = create_conf_file(use_requests, use_swagger)
                self.print_ok(f'Config file "{conf_file_path}" created')
                return True
            except Exception as ex:
                self.print_error(ex.__str__())
                return False
        return True

    def yes_no_input(self, msg=""):  # pragma: no cover
        answer = input(  # nosec
            utils.colored_text(f'{msg}{"?" if not msg.endswith("?") else ""} [Y/n] :', utils.Colors.BLUE, True)
        )
        try:
            return strtobool(answer)
        except ValueError:
            self.print_error('Invalid input, Please answer with a "Y" or "n"')
            self.yes_no_input(msg)

    @staticmethod
    def print_ok(msg=""):
        print(utils.colored_text(msg, utils.Colors.BRIGHT_GREEN, True))

    def print_verbose(self, msg=""):  # pragma: no cover
        if self.verbose:
            print(msg)

    @staticmethod
    def print_error(msg=""):  # pragma: no cover
        print(utils.colored_text(msg, utils.Colors.BRIGHT_RED, True))

    def exit_with_error(self, msg=""):  # pragma: no cover
        self.print_error(msg)
        sys.exit(2)

    def exit_ok(self, msg=""):  # pragma: no cover
        self.print_ok(msg)
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    cmd = Command(arguments=sys.argv[1:], autorun=False)
    cmd.run()
