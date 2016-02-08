from mechanic.update import Update
from mechanic.observer import Observer
from mechanic.storage import Storage
from mechanic.ui.windows.notification import UpdateNotificationWindow


class UpdateObserver(Observer):
    """Observe application launch to check for updates"""

    def __init__(self, *events):
        self.add('check_for_updates', *events)

    def check_for_updates(self, info):
        """Open updates window unless ran in last hour"""
        if self.should_check_for_updates():
            UpdateNotificationWindow.initialize_in_thread()

    def should_check_for_updates(self):
        return bool(Storage.get('check_on_startup')) and \
            not Update.checked_recently()
