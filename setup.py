# -*- coding: utf-8 -*-
# Copyright (c) 2018 by Alberto Vara <albertovara@paradigmadigital.com>
import codecs
import os

from setuptools import setup, find_packages

author = __import__('pyms').__author__
author_email = __import__('pyms').__email__
version = __import__('pyms').__version__

if os.path.exists('README.md'):
    long_description = codecs.open('README.md', 'r', 'utf-8').read()
else:
    long_description = ''

# parse_requirements() returns generator of pip.req.InstallRequirement objects
with open('requirements.txt') as f:
    required = [lib for lib in f.read().splitlines() if not lib.startswith("-e")]

setup(
    name="py-ms",
    version=version,
    author=author,
    author_email=author_email,
    description="",
    long_description=long_description,
    classifiers=[
        'Development Status :: {} - In progress'.format(version),
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    license="Proprietary",
    platforms=["any"],
    keywords="",
    url='',
    test_suite='nose.collector',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    zip_safe=True,
)