from mechanic.ui.windows.base import BaseWindow
from mechanic.ui.tabs import *


class MechanicWindow(BaseWindow):
    window_title = "Mechanic"

    def __init__(self, *args, **kwargs):
        self.toolbar.add(InstallTab)
        self.toolbar.add(UpdatesTab)
        self.toolbar.add(RegisterTab)
        self.toolbar.add(SettingsTab)
