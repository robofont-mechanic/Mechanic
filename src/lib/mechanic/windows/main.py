from mechanic.windows.base import BaseWindow
from mechanic.tabs import *


class MechanicWindow(BaseWindow):
    window_title = "Mechanic"

    def __init__(self, *args, **kwargs):
        super(MechanicWindow, self).__init__(*args, **kwargs)

        self.toolbar.add_item(InstallTab)
        self.toolbar.add_item(UpdatesTab)
        self.toolbar.add_item(RegisterTab)
        self.toolbar.add_item(SettingsTab)

        self.open()
