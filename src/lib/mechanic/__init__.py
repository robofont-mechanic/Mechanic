import os
import sys


mechanic_path = os.path.dirname(__file__)
lib_path = os.path.abspath(os.path.join(mechanic_path, "..", "packages"))
if lib_path not in sys.path:
    sys.path.append(lib_path)

__all__ = ["models", "views", "helpers"]

default_registry = "http://www.robofontmechanic.com"
