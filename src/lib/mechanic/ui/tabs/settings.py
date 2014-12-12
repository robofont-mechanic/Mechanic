from AppKit import *
from vanilla import *
from vanilla.dialogs import getFile

from mechanic.ui.lists.settings import SettingsList
from mechanic.ui.tabs.base import BaseTab
from mechanic.ui.fields.setting_check_box import SettingCheckBox


class SettingsTab(BaseTab):
    title = "Settings"
    image = "prefToolbarMisc"
    identifier = "settings"

    updates_label = "Check for updates on startup"
    minor_updates_label = "Ignore patch updates on startup"

    def setup(self):
        self.content.list = SettingsList((0, 60, -0, -0))

        self.content.startup = SettingCheckBox((0, 0, -0, 0),
                                               self.updates_label,
                                               "check_on_startup")

        self.content.patches = SettingCheckBox((0, 25, -0, 0),
                                               self.minor_updates_label,
                                               "ignore_patch_updates")
