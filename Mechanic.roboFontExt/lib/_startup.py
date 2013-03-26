import os, sys, time

lib_path = os.path.join(os.path.dirname(__file__), "modules")
if not lib_path in sys.path: sys.path.append(lib_path)

from mojo.events import addObserver
from mechanic.helpers import Storage
from mechanic.views import UpdatesWindow

class MechanicObserver:
    
    def __init__(self):
        addObserver(self, 'checkForUpdates', 'applicationDidFinishLaunching')
        
    def checkForUpdates(self, info):
        last_run = Storage.get('last_run')
        if last_run is None or last_run < time.time() - (60 * 60):
            UpdatesWindow().open()
            Storage.set('last_run', time.time())

Storage.setDefaults()
MechanicObserver()