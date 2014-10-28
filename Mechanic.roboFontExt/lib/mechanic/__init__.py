import os
import sys


lib_path = os.path.join(os.path.dirname(__file__), "modules")
if lib_path not in sys.path:
    sys.path.append(lib_path)

__all__ = ["models", "views", "helpers"]

default_registry = "http://www.robofontmechanic.com/api/v1/registry.json"
