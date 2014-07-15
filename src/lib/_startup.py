import time

from mojo.events import addObserver
from mechanic.helpers import Storage
from mechanic.views import UpdateNotificationWindow

class MechanicObserver:
    """Observe application launch to check for updates"""

    def __init__(self):
        addObserver(self, 'checkForUpdates', 'applicationDidFinishLaunching')
        addObserver(self, 'checkForUpdates', 'applicationDidBecomeActive')

    def checkForUpdates(self, info):
        """Open updates window unless ran in last hour"""
        last_run = Storage.get('last_run')
        if last_run is None or last_run < time.time() - (60 * 60):
            UpdateNotificationWindow.with_new_thread()
            Storage.set('last_run', time.time())

Storage.setDefaults()
MechanicObserver()
