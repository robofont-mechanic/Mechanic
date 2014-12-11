import time
from vanilla import *

from mechanic.update import Update
from mechanic.ui import progress
from mechanic.ui.lists.update import UpdateList
from mechanic.ui.tabs.base import BaseTab


class UpdatesTab(BaseTab):
    title = "Updates"
    image = "toolbarScriptReload"
    identifier = "updates"

    def setup(self):
        self.updateableList = UpdateList((20,20,-20,-50),
                                         editCallback=self.updateUpdateButtonLabel)
        self.addUpdatedAt()
        self.addUpdateButton()

    @progress.each('installable')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('repositoryWillExtractDownload',
                   'Extracting {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def update(self, sender):
        for extension in self.installable:
            extension.update()

        self.updateList(True)

    def activate(self):
        self.parent.w.setDefaultButton(self.updateButton)
        self.updateList()

    def updateList(self, force=False):
        self.updateableList.refresh(force=force)
        self.updateUpdatedAt()

    def addUpdatedAt(self):
        self.updatedAt = TextBox((20,-31,-20,20), "", sizeStyle="small")
        self.updateUpdatedAt()

    def updateUpdatedAt(self):
        updated = Update.last_checked()
        if updated:
            fmt = time.strftime('%d %b %Y, %H:%M', time.localtime(updated))
            self.updatedAt.set("Last checked: %s" % fmt)
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

    @property
    def installable(self):
        return self.updateableList.selected_extensions
