import os
import plistlib


class Configuration(dict):

    namespace = "com.robofontmechanic"

    def __init__(self, path):
        if os.path.exists(path):
            for key, value in plistlib.readPlist(path).items():
                self[key] = value

    def namespaced(self, key):
        return self.get('.'.join([self.namespace, key]))

    def deprecated(self, key):
        return self.get(key)
