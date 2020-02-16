import logging
import os

from pyms.constants import LOGGER_NAME

files_cached = {}

logger = logging.getLogger(LOGGER_NAME)


class LoadFile:
    default_file = None
    file_env_location = None
    path = None

    def __init__(self, path, env_var, default_filename):
        self.path = path
        self.file_env_location = env_var
        self.default_file = default_filename

    def get_file(self, fn=None):
        return self._get_conf_from_file(fn) or self._get_conf_from_env(fn)

    def put_file(self, content, mode="w"):
        self.get_or_setpath()
        file_to_write = open(self.path, mode)
        file_to_write.write(content)  # The key is type bytes still
        file_to_write.close()

    def get_or_setpath(self):
        config_file = os.environ.get(self.file_env_location, self.default_file)
        logger.debug("Searching file in ENV[{}]: {}...".format(self.file_env_location, config_file))
        self.path = config_file
        return self.path

    def _get_conf_from_env(self, fn=None):
        self.get_or_setpath()
        return self._get_conf_from_file(fn)

    def _get_conf_from_file(self, fn=None):
        if not self.path or not os.path.isfile(self.path):
            logger.debug("File {} NOT FOUND".format(self.path))
            return {}
        if self.path not in files_cached:
            logger.debug("[CONF] Configmap {} found".format(self.path))
            if fn:
                files_cached[self.path] = fn(self.path)
            else:
                file_to_read = open(self.path, 'rb')
                content = file_to_read.read()  # The key will be type bytes
                file_to_read.close()
                files_cached[self.path] = content
        return files_cached[self.path]

    def reload(self, fn=None):
        files_cached.pop(self.path, None)
        return self.get_file(fn)
