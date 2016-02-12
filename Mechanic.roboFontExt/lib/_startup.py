from AppKit import NSThread

from mechanic import logger
from mechanic.bus import Bus
from mechanic.storage import Storage
from mechanic.observers.update import UpdateObserver

from lib.tools.notifications import SelectorWrapper

Storage.set_defaults(ignore={},
                     update_cache={},
                     check_on_startup=True,
                     ignore_patch_updates=False)


UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')
