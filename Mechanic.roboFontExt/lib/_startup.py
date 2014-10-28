from mechanic.env import default_registry
from mechanic.storage import Storage
from mechanic.observer import UpdateObserver


Storage.set_defaults(ignore={},
                     cache={},
                     check_on_startup=True,
                     ignore_patch_updates=False,
                     registries=[default_registry])

UpdateObserver('applicationDidFinishLaunching',
               'applicationDidBecomeActive')
