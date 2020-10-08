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
    'flask>=1.1.2',
    'python-json-logger>=2.0.0',
    'pyyaml>=5.3.1',
    'anyconfig>=0.9.11',
    'cryptography>=3.1.1',
]

install_crypt_requires = [
    'cryptography>=3.1.1',
]

install_aws_requires = [
    'boto3>=1.15.6',
]


install_request_requires = [
    'requests>=2.24.0',
]
install_swagger_requires = [
    'connexion[swagger-ui]>=2.7.0',
    'swagger-ui-bundle>=0.0.6',
    'semver>=2.10.1',
    'prance>=0.18.2',
]

install_traces_requires = [
    'jaeger-client>=4.3.0',
    'flask-opentracing>=1.1.0',
    'opentracing>=2.1',
    'opentracing-instrumentation>=3.2.1',
    'tornado>=4.3,<6.0'
]

install_metrics_requires = [
    'prometheus_client>=0.8.0',
]

install_tests_requires = [
    'requests-mock>=1.8.0',
    'coverage>=5.3',
    'pytest>=6.1.0',
    'pytest-cov>=2.10.1',
    'pylint>=2.6.0',
    'flake8>=3.8.2',
    'tox>=3.20.0',
    'bandit>=1.6.2',
    'mkdocs>=1.1.2',
    'mkdocs-material>=6.0.0',
    'lightstep>=4.4.8',
    'safety==1.9.0',
    'mypy>=0.782'
]

install_all_requires = (install_request_requires + install_swagger_requires +
                        install_traces_requires + install_metrics_requires + install_crypt_requires +
                        install_aws_requires)

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
        'pytest-runner>=5.2',
    ],
    install_requires=install_min_requires,
    extras_require={
        'all': install_all_requires,
        'request': install_request_requires,
        'swagger': install_swagger_requires,
        'traces': install_traces_requires,
        'metrics': install_metrics_requires,
        'crypt': install_crypt_requires,
        'aws': install_aws_requires,
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
