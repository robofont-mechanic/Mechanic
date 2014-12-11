from mojo.events import addObserver
from mechanic.ui.windows.notification import UpdateNotificationWindow
from mechanic.update import Update


class UpdateObserver(object):
    """Observe application launch to check for updates"""

    def __init__(self, *events):
        for event in events:
            addObserver(self, 'check_for_updates', event)

    def check_for_updates(self, info):
        """Open updates window unless ran in last hour"""
        if not Update.checked_recently():
            UpdateNotificationWindow.with_new_thread()
