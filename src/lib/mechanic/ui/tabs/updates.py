import time
from vanilla import Button, TextBox

from mechanic.threaded import ThreadedObject
from mechanic.update import Update
from mechanic.ui import progress
from mechanic.ui.overlay import Overlay
from mechanic.ui.lists.update import UpdateList
from mechanic.ui.tabs.base import BaseTab


class UpdatesTab(BaseTab, ThreadedObject):
    title = "Updates"
    image = "toolbarScriptReload"
    identifier = "updates"

    def setup(self):
        self.list = UpdateList((20, 20, -20, -60),
                               editCallback=self.update_interface,
                               refreshCallback=self.update_interface)

        self.content.updated_at_text = UpdatedTimeTextBox((100, -18, -0, 20),
                                                          sizeStyle="small")

        self.content.update_button = UpdateButton((-140, -22, 140, 20),
                                                  callback=self.install_updates)


        self.content.refresh_button = Button((0, -22, 90, 20), "Refresh",
                                             callback=self.in_thread.update_list)

        self.update_interface()

    def activate(self):
        self.set_default_button(self.content.update_button)
        self.in_thread.update_list()

    @progress.each('installable')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def install_updates(self, sender=None):
        for extension in self.installable:
            extension.update()

        self.in_thread.update_list()

    def update_list(self, force=False):
        if self.list.is_refreshing:
            return None

        try:
            self.update_progress = Overlay("Checking for updates...",
                                           (20, 20, -20, -60),
                                           opacity=0.6,
                                           offset=90)
            self.content.refresh_button.enable(False)
            self.list.refresh(force=force)
            self.enable()
        except UpdateList.ConnectionError:
            self.disable("Couldn't connect to the internet...")
        finally:
            del self.update_progress
            self.content.refresh_button.enable(True)

    def update_interface(self, sender=None):
        self.content.updated_at_text.update()
        self.content.update_button.update(len(self.list.selected))

    def disable(self, *args, **kwargs):
        self.list.enable(False)
        super(UpdatesTab, self).disable(*args, **kwargs)

    def enable(self, *args, **kwargs):
        self.list.enable(True)
        super(UpdatesTab, self).enable(*args, **kwargs)

    @property
    def installable(self):
        return self.list.selected


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
            fmt = time.strftime('%d %b %Y, %H:%M:%S', time.localtime(updated))
            self.set("Last checked: %s" % fmt)
        else:
            self.set('')
