import importlib
import importlib.util

from pyms.exceptions import PackageNotExists


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def import_package(package):
    return importlib.import_module(package)


def check_package_exists(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        raise PackageNotExists("{package} is not installed. try with pip install -U {package}".format(package=package_name))
    return True
