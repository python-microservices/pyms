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
        return self._get_conf_from_env(fn) or self._get_conf_from_file(self.path, fn)

    def put_file(self, content, mode="w"):
        path = self.get_path_from_env()
        file_to_write = open(path, mode)
        file_to_write.write(content)  # The key is type bytes still
        file_to_write.close()

    def get_path_from_env(self):
        config_file = os.environ.get(self.file_env_location, self.default_file)
        logger.debug("Searching file in ENV[{}]: {}...".format(self.file_env_location, config_file))
        return config_file

    def _get_conf_from_env(self, fn=None):
        path = self.get_path_from_env()
        return self._get_conf_from_file(path, fn)

    def _get_conf_from_file(self, path, fn=None):
        if path and os.path.isdir(path):
            path = os.path.join(path, self.default_file)

        if not path or not os.path.isfile(path):
            logger.debug("File {} NOT FOUND".format(path))
            return {}
        if path not in files_cached:
            logger.debug("[CONF] Configmap {} found".format(path))
            self.path = path
            if fn:
                files_cached[path] = fn(path)
            else:
                file_to_read = open(path, 'rb')
                content = file_to_read.read()  # The key will be type bytes
                file_to_read.close()
                files_cached[path] = content
        return files_cached[path]

    def reload(self, fn=None):
        files_cached.pop(self.path, None)
        return self.get_file(fn)
