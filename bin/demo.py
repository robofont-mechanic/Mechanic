from mechanic.registry import Registry
from mechanic.ui.windows.main import MechanicWindow
from mechanic.ui.windows.notification import UpdateNotificationWindow

window = MechanicWindow().open('install')
tab = window.current_tab.view
table = tab.list

table.set(Registry('http://www.robofontmechanic.com').extensions())
tab.enable()

def dummy_updates(self, *args, **kwargs): return ['updates']

UpdateNotificationWindow.get_updates = dummy_updates
UpdateNotificationWindow()
