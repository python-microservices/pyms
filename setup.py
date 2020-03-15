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

install_min_requires = [
    'flask>=1.1.1',
    'python-json-logger>=0.1.10',
    'pyyaml>=5.1.2',
    'anyconfig>=0.9.8',
    'cryptography>=2.8',
]

install_request_requires = [
    'requests>=2.23.0',
]
install_swagger_requires = [
    'swagger-ui-bundle>=0.0.2',
    'connexion[swagger-ui]>=2.6.0',
    'swagger-ui-bundle>=0.0.6',
    'anyconfig>=0.9.8',
]

install_traces_requires = [
    'jaeger-client>=4.3.0',
    'flask-opentracing>=1.1.0',
    'opentracing>=2.1',
    'opentracing-instrumentation>=3.2.1',
    'tornado>=4.3,<6.0'
]

install_metrics_requires = [
    'prometheus_client>=0.7.1',
]

install_tests_requires = [
    'requests-mock>=1.7.0',
    'coverage>=5.0.3',
    'pytest>=5.3.5',
    'pytest-cov>=2.8.1',
    'pylint>=2.4.4',
    'flake8>=3.7.9',
    'tox>=3.14.5',
    'bandit>=1.6.2',
    'mkdocs>=1.1',
    'mkdocs-material>=4.6.3',
    'lightstep>=4.4.3',
]

install_all_requires = (install_request_requires + install_swagger_requires +
                        install_traces_requires + install_metrics_requires)

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
        "Programming Language :: Python :: 3.8",
    ],
    license="License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    platforms=["any"],
    keywords="",
    url='https://github.com/python-microservices/pyms/',
    packages=find_packages(
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', '*.examples', '*.examples.*', 'examples.*', 'examples']),
    setup_requires=[
        'pytest-runner>=2.0,<3dev',
    ],
    install_requires=install_min_requires,
    extras_require={
        'all': install_all_requires,
        'request': install_request_requires,
        'swagger': install_swagger_requires,
        'traces': install_traces_requires,
        'metrics': install_metrics_requires,
        'tests': install_tests_requires,
    },
    tests_require=install_all_requires + install_tests_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyms = pyms.cmd.main:Command'
        ]
    },
    zip_safe=True,
)
