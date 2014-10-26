from mechanic import default_registry
from mechanic.storage import Storage
from mechanic.observer import UpdateObserver


Storage.set_defaults(ignore={},
                     check_on_startup=True,
                     cache={},
                     cached_at=0.0,
                     ignore_patch_updates=False,
                     registries=[default_registry])

UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')
