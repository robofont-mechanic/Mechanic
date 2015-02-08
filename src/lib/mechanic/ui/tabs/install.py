import requests

from vanilla import *
from mojo.extensions import ExtensionBundle

from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.ui import progress
from mechanic.ui.tabs.base import BaseTab
from mechanic.ui.lists.installation import InstallationList


class InstallTab(BaseTab):
    title = "Install"
    image = "toolbarRun"
    identifier = "install"

    tab_size = (500, 400)

    def setup(self):
        # Can't use self.content here because of stacking issues with Overlay
        self.list = InstallationList((20, 20, -20, -60),
                                     selectionCallback=self.update_buttons)

        self.content.uninstall_button = Button((-270, -22, 100, 20),
                                               "Uninstall",
                                               callback=self.uninstall)

        self.content.install_button = Button((-160, -22, 160, 20),
                                             "Install Extension",
                                             callback=self.install)

        self.update_buttons()


    @progress.each('content.list.selected')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('repositoryWillExtractDownload',
                   'Extracting {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def install(self, sender):
        for item in self.list.selected:
            Extension.install_remote(repository=item['repository'],
                                     name=item['name'],
                                     filename=item['filename'])

        self.list.refresh()
        self.update_buttons()

    @progress.each('uninstallable')
    @progress.tick('extensionWillUninstall',
                   'Uninstalling {extension.bundle.name}')
    def uninstall(self, sender):
        for extension in self.uninstallable:
            extension.uninstall()

        self.list.refresh()
        self.update_buttons()

    def activate(self):
        self.update_list()

    def update_list(self):
        try:
            self.list.set(Registry.all())
            self.enable()
        except requests.ConnectionError:
            self.disable("Couldn't connect to the registry server...")

        self.set_default_button(self.content.install_button)

    def disable(self, *args, **kwargs):
        self.list.enable(False)
        super(InstallTab, self).disable(*args, **kwargs)

    def enable(self, *args, **kwargs):
        self.list.enable(True)
        super(InstallTab, self).enable(*args, **kwargs)

    def update_buttons(self, sender=None):
        self.update_install_button_label()
        self.update_uninstall_button_label()

    def update_uninstall_button_label(self, sender=None):
        self.content.uninstall_button.enable(len(self.uninstallable) > 0)

    def update_install_button_label(self, sender=None):
        selections = self.list.getSelection()
        self.content.install_button.enable(selections)
        if len(selections) > 1:
            label = "Install %d Extensions" % len(selections)
        elif len(selections) is 1:
            label = "Install %d Extension" % len(selections)
        else:
            label = "Install Extensions"
        self.content.install_button.setTitle(label)

    @property
    def uninstallable(self):
        filenames = [item['filename'] for item in self.list.selected]
        names = [filename.split("/")[-1] for filename in filenames]
        extensions = [Extension(name=name) for name in names]
        return [ext for ext in extensions if ext.installed]
