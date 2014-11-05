from AppKit import NSImage
from vanilla import *
from vanilla.dialogs import getFile

from mechanic.ui import progress
from mechanic.ui.font import Font
from mechanic.storage import Storage
from mechanic.extension import Extension
from mechanic.update import Updates
from mechanic.windows.base import BaseWindow


class UpdateNotificationWindow(BaseWindow):
    window_title = "Extension Updates"

    @classmethod
    def with_new_thread(cls):
        import threading
        threading.Thread(target=cls).start()

    def __init__(self, force=False):
        super(UpdateNotificationWindow, self).__init__()

        skip_patch = bool(Storage.get('ignore_patch_updates'))
        self.updater = Updates()
        self.updates = self.updater.all(force,
                                        skip_patch_updates=skip_patch)

        # TODO: Make this use exceptions
        if self.updater.unreachable:
            print "Mechanic: Couldn't connect to the internet"
            return

        if self.updates:
            self.create_image()

            self.w.title = TextBox((105, 20, -20, 20), self.title)

            self.w.explanation = TextBox((105, 45, -20, 50), self.explanation)

            self.w.updateButton = Button((-150, -40, 130, 20),
                                         "Install Updates",
                                         callback=self.update)
            self.w.cancelButton = Button((-255, -40, 90, 20),
                                         "Not Now",
                                         callback=self.cancel)
            self.w.showDetailsButton = Button((105, -40, 110, 20),
                                              "Show Details",
                                              callback=self.show_details)
            self.w.setDefaultButton(self.w.updateButton)

            self.w.open()
        else:
            print "Mechanic: All extensions are up to date."

    @progress.each('updates')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('repositoryWillExtractDownload',
                   'Extracting {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def update(self, sender):
        for extension in self.updates:
            extension.update()

        self.progress.close()

    def show_details(self, sender):
        self.w.close()
        MechanicWindow('updates')

    def cancel(self, sender):
        self.w.close()

    def create_image(self):
        image = NSImage.imageNamed_("ExtensionIcon")
        self.w.image = ImageView((15, 15, 80, 80), scale='fit')
        if image:
            self.w.image.setImage(imageObject=image)

    @property
    def title(self):
        text = "Updates are available for %d of your extensions."
        return Font.string(text=text % len(self.updates),
                           style="bold")

    @property
    def explanation(self):
        text = "If you don't want to update now, choose Extensions > Mechanic > Updates when you're ready to install."
        Font.string(text=text, size=11)
