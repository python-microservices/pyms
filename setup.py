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

install_requires = [
    'flask<1.1,>=1.0.2',
    'anyconfig<1.0.0,>=0.9.7',
    'python-json-logger<0.2.0,>=0.1.10',
    'connexion[swagger-ui]<2.2.0,>=2.1.0',
    'Flask-OpenTracing<0.3.0,>=0.2.0',
    'jaeger-client<3.13.0,>=3.12.0'
]

tests_require = [
    'coverage<4.6.0,>=4.5.2',
    'mock<2.1.0,>=2.0.0',
    'nose<1.4.0,>=1.3.7',
    'pylint<2.3.0,>=2.2.2',
    'tox<3.7.0>=3.6.0',
    'requests_mock<1.6.0,>=1.5.2'
]

setup(
    name="py-ms",
    version=version,
    author=author,
    author_email=author_email,
    description="",
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    platforms=["any"],
    keywords="",
    url='',
    test_suite='nose.collector',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=True,
)
