from AppKit import *
from vanilla import *

from mechanic.ui.lists.settings import SettingsList
from mechanic.ui.tabs.base import BaseTab
from mechanic.ui.fields.setting_check_box import SettingCheckBox


class SettingsTab(BaseTab):
    title = "Settings"
    image = "prefToolbarMisc"
    identifier = "settings"

    def setup(self):
        self.list = SettingsList((20, 80, -20, -20))

        self.startup = SettingCheckBox((23, 20, -20, 22),
                                       "Check for updates on startup",
                                       "check_on_startup")

        self.patches = SettingCheckBox((23, 45, -20, 22),
                                       "Ignore patch updates on startup",
                                       "ignore_patch_updates")
