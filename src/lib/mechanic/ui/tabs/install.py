import webbrowser
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
    
    tabSize = (500, 400)
    disabledText = "Couldn't connect to the registry server..."
    
    def setup(self):
        self.list = InstallationList((20,20,-20,-50),
                                     selectionCallback=self.update_buttons,
                                     doubleClickCallback=self.open_repo)
        self.uninstall_button = Button((-290,-35,100,20), "Uninstall",
                                       callback=self.uninstall)
        self.install_button = Button((-180,-35,160,20), "Install Extension",
                                     callback=self.install)
        self.update_buttons()


    @progress.each('list.selected')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
    @progress.tick('repositoryWillExtractDownload',
                   'Extracting {repository.repo}')
    @progress.tick('extensionWillInstall',
                   'Installing {extension.bundle.name}')
    def install(self, sender):
        for item in self.list.selected:
            remote = GithubRepo(item['repository'],
                                name=item['name'],
                                filename=item['filename'])
            Extension(path=remote.download()).install()

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
        self.updateList()

    def updateList(self):
        if not self.list.get():
            try:
                extensions = Registry().all()
                self.enable()
            except:
                extensions = []
                self.disable()
            self.list.set(extensions)
        else:
            self.list.refresh()

        self.w.setDefaultButton(self.install_button)

    def disable(self):
        self.list.enable(False)
        super(InstallTab, self).disable()

    def enable(self):
        self.list.enable(True)
        super(InstallTab, self).enable()

    def open_repo(self, sender):
        for item in self.list.selected:
            webbrowser.open('http://github.com/%s' % item['repository'])

    def update_buttons(self, sender=None):
        self.update_install_button_label()
        self.update_uninstall_button_label()

    def update_uninstall_button_label(self, sender=None):
        self.uninstall_button._nsObject.setEnabled_(len(self.uninstallable) > 0)

    def update_install_button_label(self, sender=None):
        selections = self.list.getSelection()
        self.install_button._nsObject.setEnabled_(selections)
        if len(selections) > 1:
            label = "Install %d Extensions" % len(selections)
        elif len(selections) is 1:
            label = "Install %d Extension" % len(selections)
        else:
            label = "Install Extensions"
        self.install_button.setTitle(label)

    @property
    def uninstallable(self):
        filenames = [item['filename'] for item in self.list.selected]
        names = [filename.split("/")[-1] for filename in filenames]
        extensions = [Extension(name=name) for name in names]
        return [ext for ext in extensions if ext.installed]
