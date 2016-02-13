from mechanic import logger
from mechanic.bus import Bus
from mechanic.event_caller import EventCaller
from mechanic.storage import Storage
from mechanic.observers.update import UpdateObserver
from mechanic.ui.windows.notification import UpdateNotificationWindow


Storage.set_defaults(ignore={},
                     update_cache={},
                     check_on_startup=True,
                     ignore_patch_updates=False)


UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')


EventCaller('newUpdatesFound', UpdateNotificationWindow)
