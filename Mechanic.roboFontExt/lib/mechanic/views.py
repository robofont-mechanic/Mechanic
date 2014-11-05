from AppKit import NSImage
from vanilla import *
from vanilla.dialogs import getFile
from mojo.extensions import ExtensionBundle

from mechanic.font import Font
from mechanic.storage import Storage
from mechanic.models import Extension, Updates
from mechanic.ui.windows.base import BaseWindow
from mechanic.tabs import *
from mechanic.repositories.github import GithubRepo


class UpdateNotificationWindow(BaseWindow):
    window_title = "Extension Updates"

    explanation = "If you don't want to update now, choose Extensions > Mechanic > Updates when you're ready to install."
    up_to_date = 'All extensions are up to date.'
    updates_available = "Updates are available for %d of your extensions."

    @classmethod
    def with_new_thread(cls):
        import threading
        threading.Thread(target=cls).start()

    @property
    def title(self):
        return Font.string(text=self.updates_available % len(self.updates),
                           style="bold")

    def __init__(self, force=False):
        super(UpdateNotificationWindow, self).__init__()

        skip_patch = bool(Storage.get('ignore_patch_updates'))
        self.updater = Updates()
        self.updates = self.updater.all(force, skip_patch_updates=skip_patch)

        # TODO: Make this use exceptions
        if self.updater.unreachable:
            print "Mechanic: Couldn't connect to the internet"
            return

        if self.updates:
            self.create_image()

            self.w.title = TextBox((105, 20, -20, 20), self.title)

            explanation = Font.string(text=self.explanation, size=11)
            self.w.explanation = TextBox((105, 45, -20, 50), explanation)

            self.w.updateButton = Button((-150, -40, 130, 20),
                                         "Install Updates",
                                         callback=self.update)
            self.w.cancelButton = Button((-255, -40, 90, 20),
                                         "Not Now",
                                         callback=self.cancel)
            self.w.showDetailsButton = Button((105, -40, 110, 20),
                                              "Show Details",
                                              callback=self.showDetails)
            self.w.setDefaultButton(self.w.updateButton)

            self.w.open()
        else:
            print "Mechanic: %s" % self.up_to_date

    def cancel(self, sender):
        self.w.close()

    def update(self, sender):            
        ticks = len(self.updates) * Extension.ticks_per_download
        self.progress = self.startProgress('Updating', ticks)

        for extension in self.updates:
            extension.update()

        self.progress.close()

    def showDetails(self, sender):
        self.w.close()
        MechanicWindow('updates')

    def create_image(self):
        image = NSImage.imageNamed_("ExtensionIcon")
        self.w.image = ImageView((15, 15, 80, 80), scale='fit')
        if image:
            self.w.image.setImage(imageObject=image)


class MechanicWindow(BaseWindow):
    window_title = "Mechanic"

    def __init__(self, *args, **kwargs):
        super(MechanicWindow, self).__init__(*args, **kwargs)

        self.toolbar.add_item(InstallTab)
        self.toolbar.add_item(UpdatesTab)
        self.toolbar.add_item(RegisterTab)
        self.toolbar.add_item(SettingsTab)

        self.open()
