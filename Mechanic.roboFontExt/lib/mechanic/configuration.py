import os
import plistlib


class Configuration(dict):

    def __init__(self, path):
        if os.path.exists(path):
            for key, value in plistlib.readPlist(path).items():
                self[key] = value
