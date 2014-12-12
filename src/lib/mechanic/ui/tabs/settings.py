from AppKit import *
from vanilla import *
from vanilla.dialogs import getFile

from mechanic.storage import Storage
from mechanic.ui.lists.settings import SettingsList
from mechanic.ui.tabs.base import BaseTab


class SettingsTab(BaseTab):
    title = "Settings"
    image = "prefToolbarMisc"
    identifier = "settings"

    updates_label = "Check for updates on startup"
    minor_updates_label = "Ignore patch updates on startup"
    check_on_startup = Storage.get("check_on_startup")

    def setup(self):                
        self.list = SettingsList((0, 60, -0, -0),
                                 editCallback=self.update)

        self.checkForUpdates = CheckBox((0, 0, -0, 0),
                                        self.updates_label,
                                        value=Storage.get("check_on_startup"),
                                        callback=self.saveCheckForUpdates)

        self.ignorePatchUpdates = CheckBox((0, 25, -0, 0),
                                           self.minor_updates_label,
                                           value=Storage.get("ignore_patch_updates"),
                                           callback=self.saveIgnorePatchUpdates)

    def saveCheckForUpdates(self, sender):
        Storage.set("check_on_startup", 
            bool(self.checkForUpdates.get()))

    def saveIgnorePatchUpdates(self, sender):
        Storage.set("ignore_patch_updates", 
            bool(self.ignorePatchUpdates.get()))

    def update(self, sender):
        ignore = Storage.get("ignore")
        for row in self.list.get():
            if not row["check_for_updates"]:
                ignore[row["name"]] = True
            elif row["name"] in ignore:
                del ignore[row["name"]]
        Storage.set('ignore', ignore)
