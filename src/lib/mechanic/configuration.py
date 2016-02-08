import os
import plistlib

from mechanic import logger


class Configuration(dict):

    namespace = "com.robofontmechanic.Mechanic"

    def __init__(self, path):
        if os.path.exists(path):
            for key, value in plistlib.readPlist(path).items():
                self[key] = value

    def namespaced(self, key):
        return self.get(self.namespace, {}).get(key)

    def deprecated(self, key):
        value = self.get(key)
        if value is not None:
            logger.info('%s is using the deprecated `%s` configuration, which will not be supported in Mechanic 2.',
                        self.get('name'),
                        key)
        return value
