from mechanic import logger
from mechanic.bus import Bus
from mechanic.threaded import Threaded
from mechanic.update import Update
from mechanic.observer import Observer
from mechanic.storage import Storage


class UpdateObserver(Observer):
    """Observe application launch to check for updates"""

    def __init__(self, *events):
        self.add('check_for_updates_in_thread', *events)

    def check_for_updates_in_thread(self, info):
        Threaded(self).check_for_updates()

    def check_for_updates(self):
        """Open updates window unless ran in last hour"""

        if self.should_check_for_updates():
            try:
                skip_patches = bool(Storage.get('ignore_patch_updates'))
                updates = Update.all(force=True, skip_patches=skip_patches)
            except Update.ConnectionError:
                logger.info("Couldn't connect to the internet")
                return

            if updates:
                logger.info("%d new updates found", len(updates))

                Bus().emit("newUpdatesFound", updates)
            else:
                logger.info("No new updates found")
        else:
            logger.info("Skipping a check for new updates")

    def should_check_for_updates(self):
        return bool(Storage.get('check_on_startup')) and \
            not Update.checked_recently()
