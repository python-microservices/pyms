# -*- coding: utf-8 -*-
# Copyright (c) 2018 by Alberto Vara <albertovara@paradigmadigital.com>
import codecs
import os

import json
from setuptools import setup, find_packages

author = __import__('pyms').__author__
author_email = __import__('pyms').__email__
version = __import__('pyms').__version__

if os.path.exists('README.md'):
    long_description = codecs.open('README.md', 'r', 'utf-8').read()
else:
    long_description = ''



install_requires = []
tests_require = []
if os.path.exists('Pipfile.lock'):
    with open('Pipfile.lock') as fd:
        lock_data = json.load(fd)
        install_requires = [
            package_name + package_data['version']
            for package_name, package_data in lock_data['default'].items()
        ]
        tests_require = [
            package_name + package_data['version']
            for package_name, package_data in lock_data['develop'].items()
        ]

setup(
    name="py-ms",
    version=version,
    author=author,
    author_email=author_email,
    description="Library of utils to create REST Python Microservices",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    platforms=["any"],
    keywords="",
    url='https://github.com/python-microservices/pyms/',
    test_suite='nose.collector',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=True,
)
