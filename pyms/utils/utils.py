import importlib
import importlib.util
from typing import Union, Text

from pyms.exceptions import PackageNotExists


class Colors:
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    MAGENTA = "\033[35m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_YELLOW = "\033[93m"


def import_from(module: Text, name: Text):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def import_package(package: Text):
    return importlib.import_module(package)


def check_package_exists(package_name: Text) -> Union[Exception, bool]:
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        raise PackageNotExists(
            "{package} is not installed. try with pip install -U {package}".format(package=package_name))
    return True


def colored_text(msg, color: Colors, bold=False):
    result = "{}{}{}".format(color, msg, "\033[0m")
    if bold:
        result = "{}{}".format("\033[1m", result)
    return result
