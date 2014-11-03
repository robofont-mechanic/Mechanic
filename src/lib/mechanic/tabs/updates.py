import time
from vanilla import *
from vanilla.dialogs import getFile

from mechanic.lists import *
from mechanic.models import Updates
from mechanic.tabs.base import BaseTab


class UpdatesTab(BaseTab):
    title = "Update"
    image = "toolbarScriptReload"
    identifier = "updates"

    def setup(self):
        self.addList()
        self.addUpdatedAt()
        self.addUpdateButton()

    def activate(self):
        self.parent.w.setDefaultButton(self.updateButton)
        self.updateList()

    def addList(self): 
        posSize = (20,20,-20,-50)
        self.updateableList = UpdatesList(posSize,
                                          [],
                                          editCallback=self.updateUpdateButtonLabel)

    def updateList(self, force=False):
        self.updateableList.refresh(force=force)
        self.updateUpdatedAt()

    def addUpdatedAt(self):
        self.updatedAt = TextBox((20,-31,-20,20), "", sizeStyle="small")
        self.updateUpdatedAt()

    def updateUpdatedAt(self):
        updated = Updates.last_checked()
        if updated:
            self.updatedAt.set("Last checked: %s" % time.strftime('%d %b %Y, %H:%M', time.localtime(updated)))
        else:
            self.updatedAt.set('')

    def addUpdateButton(self):
        self.updateButton = Button((-160,-35,140,20),
                                   "Update",
                                   callback=self.update)
        self.updateUpdateButtonLabel()

    def updateUpdateButtonLabel(self, sender=None):
        count = len(self.updateableList.selected)
        self.updateButton.enable(count is not 0)
        if count is 0:
            update_label = "Update"
        elif count is 1:
            update_label = "Install %d Update" % count
        else:
            update_label = "Install %d Updates" % count
        self.updateButton.setTitle(update_label)

    def update(self, sender):
        installable = self.updateableList.selected_extensions
        ticks = len(installable) * 3
        self.progress = self.startProgress('Updating', ticks)

        for extension in installable:
            extension.update()

        self.updateList(True)
        self.progress.close()
