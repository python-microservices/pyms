#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import argparse
import sys

from pyms.utils import check_package_exists, import_from
from pyms.utils.crypt import Crypt


class Command:
    config = None

    parser = None

    args = []

    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        autorun = kwargs.get("autorun", True)
        if not arguments:  # pragma: no cover
            arguments = sys.argv[1:]

        parser = argparse.ArgumentParser(description='Python Microservices')

        commands = parser.add_subparsers(title="Commands", description='Available commands', dest='command_name')

        parser_encrypt = commands.add_parser('encrypt', help='Encrypt a string')
        parser_encrypt.add_argument("encrypt", default='', type=str, help='Encrypt a string')

        parser_create_key = commands.add_parser('create-key', help='Generate a Key to encrypt strings in config')
        parser_create_key.add_argument("create_key", action='store_true',
                                       help='Generate a Key to encrypt strings in config')

        parser_startproject = commands.add_parser('startproject',
                                                  help='Generate a project from https://github.com/python-microservices/microservices-template')
        parser_startproject.add_argument("startproject", action='store_true',
                                         help='Generate a project from https://github.com/python-microservices/microservices-template')

        parser_startproject.add_argument("-b", "--branch",
                                         help='Select a branch from https://github.com/python-microservices/microservices-template')

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
            pwd = self.get_input('Type a password to generate the key file: ')
            generate_file = self.get_input('Do you want to generate a file in {}? [Y/n]'.format(path))
            generate_file = generate_file.lower() != "n"
            key = crypt.generate_key(pwd, generate_file)
            if generate_file:
                self.print_ok("File {} generated OK".format(path))
            else:
                self.print_ok("Key generated: {}".format(key))
        if self.encrypt:
            encrypted = crypt.encrypt(self.encrypt)
            self.print_ok("Encrypted OK: {}".format(encrypted))
        if self.startproject:
            check_package_exists("cookiecutter")
            cookiecutter = import_from("cookiecutter.main", "cookiecutter")
            cookiecutter('gh:python-microservices/cookiecutter-pyms', checkout=self.branch)
            self.print_ok("Created project OK")
        return True

    @staticmethod
    def print_ok(msg=""):
        print('\033[92m\033[1m ' + msg + ' \033[0m\033[0m')

    def print_verbose(self, msg=""):  # pragma: no cover
        if self.verbose:
            print(msg)

    @staticmethod
    def print_error(msg=""):  # pragma: no cover
        print('\033[91m\033[1m ' + msg + ' \033[0m\033[0m')

    def exit_with_error(self, msg=""):  # pragma: no cover
        self.print_error(msg)
        sys.exit(2)

    def exit_ok(self, msg=""):  # pragma: no cover
        self.print_ok(msg)
        sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    cmd = Command(arguments=sys.argv[1:], autorun=False)
    cmd.run()
