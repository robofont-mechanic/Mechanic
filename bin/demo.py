from mechanic.registry import Registry
from mechanic.ui.windows.main import MechanicWindow
from mechanic.ui.windows.notification import UpdateNotificationWindow

window = MechanicWindow('install')
tab = window.current_tab.view
table = tab.content.list

table.set(Registry('http://www.robofontmechanic.com').all())
tab.enable()

def dummy_updates(self, *args, **kwargs): return ['updates']

UpdateNotificationWindow.get_updates = dummy_updates
UpdateNotificationWindow()
