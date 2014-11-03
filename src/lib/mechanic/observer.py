from mojo.events import addObserver
from mechanic.windows.notification import UpdateNotificationWindow
from mechanic.models import Updates


class UpdateObserver:
    """Observe application launch to check for updates"""

    def __init__(self, *events):
        for event in events:
            addObserver(self, 'checkForUpdates', event)

    def checkForUpdates(self, info):
        """Open updates window unless ran in last hour"""
        if not Updates.checked_recently():
            UpdateNotificationWindow.with_new_thread()
