from mechanic.storage import Storage
from mechanic.observers.update import UpdateObserver


Storage.set_defaults(ignore={},
                     update_cache={},
                     check_on_startup=True,
                     ignore_patch_updates=False)


UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')
