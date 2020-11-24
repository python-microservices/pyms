"""Exceptions of the lib. Its useful """


class AttrDoesNotExistException(Exception):
    pass


class FileDoesNotExistException(Exception):
    pass


class ServiceDoesNotExistException(Exception):
    pass


class ConfigDoesNotFoundException(Exception):
    pass


class ConfigErrorException(Exception):
    pass


class PackageNotExists(Exception):
    pass


class ServiceDiscoveryConnectionException(Exception):
    pass
