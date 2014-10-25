from AppKit import *
from vanilla import *
from vanilla.dialogs import getFile
from mojo.extensions import ExtensionBundle

from mechanic.helpers import *
from mechanic.lists import *
from mechanic.models import Extension
from mechanic.tabs.base import BaseTab


class SettingsTab(BaseTab):
    title = "Settings"
    image = "prefToolbarMisc"
    identifier = "settings"
    
    updates_label = "Check for updates on startup"
    minor_updates_label = "Ignore patch updates on startup"
    check_on_startup = Storage.get("check_on_startup")

    def setup(self):                
        self.addList()
        self.checkForUpdates = CheckBox((20,15,-20,20),
                                        self.updates_label,
                                        value=Storage.get("check_on_startup"),
                                        callback=self.saveCheckForUpdates)
        self.ignorePatchUpdates = CheckBox((20,40,-20,20),
                                           self.minor_updates_label,
                                           value=Storage.get("ignore_patch_updates"),
                                           callback=self.saveIgnorePatchUpdates)

    def addList(self):
        configured = [e for e in Extension.all() if e.is_configured()]
        self.settingsList = SettingsList((20,75,-20,-20),
                                         configured,
                                         editCallback=self.update)

    def saveCheckForUpdates(self, sender):
        Storage.set("check_on_startup", 
            bool(self.checkForUpdates.get()))

    def saveIgnorePatchUpdates(self, sender):
        Storage.set("ignore_patch_updates", 
            bool(self.ignorePatchUpdates.get()))

    def update(self, sender):
        ignore = Storage.get("ignore")
        for row in self.settingsList.get():
            if not row["check_for_updates"]:
                ignore[row["name"]] = True
            elif row["name"] in ignore:
                del ignore[row["name"]]
        Storage.set('ignore', ignore)
