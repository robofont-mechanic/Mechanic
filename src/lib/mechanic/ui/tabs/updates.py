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
        self.list = UpdateList((20,20,-20,-50),
                               editCallback=self.update_interface)
        self.updated_at_text = UpdatedTimeTextBox((20,-31,-20,20),
                                                  sizeStyle="small")
        self.update_button = UpdateButton((-160,-35,140,20),
                                          callback=self.install_updates)
        self.update_interface()

    def activate(self):
        self.parent.w.setDefaultButton(self.update_button)
        self.update_list()

    @progress.each('installable')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('repositoryWillExtractDownload',
                   'Extracting {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def install_updates(self, sender=None):
        for extension in self.installable:
            extension.update()

        self.update_list(True)

    def update_list(self, force=False):
        self.list.refresh(force=force)
        self.update_interface()

    def update_interface(self, sender=None):
        self.updated_at_text.update()
        self.update_button.update(len(self.list.selected))

    @property
    def installable(self):
        return self.list.selected_extensions


class UpdateButton(Button):

    def __init__(self, posSize, **kwargs):
        super(UpdateButton, self).__init__(posSize, "", **kwargs)

    def update(self, count):
        self.enable(count is not 0)
        self.setTitle(self.label_for_count(count))

    def label_for_count(self, count):
        if count is 0:
            return "Update"
        elif count is 1:
            return "Install %d Update" % count
        else:
            return "Install %d Updates" % count


class UpdatedTimeTextBox(TextBox):

    def __init__(self, posSize, **kwargs):
        super(UpdatedTimeTextBox, self).__init__(posSize, **kwargs)
        self.update()

    def update(self):
        updated = Update.last_checked()
        if updated:
            fmt = time.strftime('%d %b %Y, %H:%M', time.localtime(updated))
            self.set("Last checked: %s" % fmt)
        else:
            self.set('')
