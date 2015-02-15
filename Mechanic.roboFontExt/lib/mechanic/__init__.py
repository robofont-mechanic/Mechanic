import os
import sys


mechanic_path = os.path.dirname(__file__)
lib_path = os.path.abspath(os.path.join(mechanic_path, ".."))
packages_path = os.path.join(lib_path, "site-packages")
if packages_path not in sys.path:
    sys.path.append(packages_path)
