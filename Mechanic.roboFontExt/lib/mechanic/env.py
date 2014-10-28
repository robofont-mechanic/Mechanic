"""
    Imports environment variables from the .env file in the root of src and
    the compiled extension.
"""

import os.path as p
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(p.abspath(p.join(p.dirname(__file__), '..', '..', '.env')))

for key, value in config.items('mechanic'):
    globals()[key] = value

del config
del ConfigParser
del p
