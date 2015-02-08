"""
    Imports environment variables from the .env file in the root of src and
    the compiled extension.
"""

import os.path as __p
import ConfigParser as __cp

__f = __p.abspath(__p.join(__p.dirname(__file__), '..', '..', '.env'))
__c = __cp.ConfigParser()
__c.read(__f)

for key, value in __c.items('mechanic'):
    globals()[key] = value

del __c
del __cp
del __p
del __f
