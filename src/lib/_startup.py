from mechanic.helpers import Storage
from mechanic.observer import UpdateObserver


Storage.set_defaults(ignore={},
                     check_on_startup=True,
                     cache={},
                     cached_at=0.0,
                     ignore_patch_updates=False)

UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')
