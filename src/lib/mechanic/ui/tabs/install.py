import requests

from vanilla import *
from vanilla.dialogs import getFile
from mojo.extensions import ExtensionBundle

from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.repositories.github import GithubRepo
from mechanic.ui import progress
from mechanic.ui.tabs.base import BaseTab
from mechanic.ui.lists.installation import InstallationList


class InstallTab(BaseTab):
    title = "Install"
    image = "toolbarRun"
    identifier = "install"

    tab_size = (500, 400)
    disabled_text = "Couldn't connect to the registry server..."

    def setup(self):
        self.content.list = InstallationList((0, 0, -0, -40),
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
        for item in self.content.list.selected:
            remote = GithubRepo(item['repository'],
                                name=item['name'],
                                filename=item['filename'])
            Extension(path=remote.download()).install()

        self.content.list.refresh()
        self.update_buttons()

    @progress.each('uninstallable')
    @progress.tick('extensionWillUninstall',
                   'Uninstalling {extension.bundle.name}')
    def uninstall(self, sender):
        for extension in self.uninstallable:
            extension.uninstall()

        self.content.list.refresh()
        self.update_buttons()

    def activate(self):
        self.update_list()

    def update_list(self):
        if not self.content.list.get():
            try:
                extensions = Registry.all()
                self.enable()
            except:
                # TODO: Make this only except the real error
                extensions = []
                self.disable()
            self.content.list.set(extensions)
        else:
            self.content.list.refresh()

        self.set_default_button(self.content.install_button)

    def disable(self):
        self.content.list.enable(False)
        super(InstallTab, self).disable()

    def enable(self):
        self.content.list.enable(True)
        super(InstallTab, self).enable()

    def update_buttons(self, sender=None):
        self.update_install_button_label()
        self.update_uninstall_button_label()

    def update_uninstall_button_label(self, sender=None):
        self.content.uninstall_button._nsObject.setEnabled_(len(self.uninstallable) > 0)

    def update_install_button_label(self, sender=None):
        selections = self.content.list.getSelection()
        self.content.install_button._nsObject.setEnabled_(selections)
        if len(selections) > 1:
            label = "Install %d Extensions" % len(selections)
        elif len(selections) is 1:
            label = "Install %d Extension" % len(selections)
        else:
            label = "Install Extensions"
        self.content.install_button.setTitle(label)

    @property
    def uninstallable(self):
        filenames = [item['filename'] for item in self.content.list.selected]
        names = [filename.split("/")[-1] for filename in filenames]
        extensions = [Extension(name=name) for name in names]
        return [ext for ext in extensions if ext.installed]
