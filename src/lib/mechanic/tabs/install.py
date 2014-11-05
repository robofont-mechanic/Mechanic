import webbrowser
import requests
from vanilla import *
from vanilla.dialogs import getFile
from mojo.extensions import ExtensionBundle

from mechanic.lists import *
from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.tabs.base import BaseTab
from mechanic.repositories.github import GithubRepo


class InstallTab(BaseTab):
    title = "Install"
    image = "toolbarRun"
    identifier = "install"
    
    tabSize = (500, 400)
    disabledText = "Couldn't connect to the registry server..."
    
    def setup(self):
        self.addList()
        self.uninstall_button = Button((-290,-35,100,20), "Uninstall",
                                       callback=self.uninstall)
        self.install_button = Button((-180,-35,160,20), "Install Extension",
                                     callback=self.install)
        self.update_buttons()

    def addList(self):
        posSize = (20,20,-20,-50)
        self.installationList = InstallationList(posSize,
                                                 [],
                                                 selectionCallback=self.update_buttons,
                                                 allowsMultipleSelection=True,
                                                 doubleClickCallback=self.open_repo)

    def updateList(self):
        if not self.installationList.get():
            try:
                extensions = Registry().all()
                self.enable()
            except:
                extensions = []
                self.disable()
            self.installationList.set(extensions)
        else:
            self.installationList.refresh()

        self.parent.w.setDefaultButton(self.install_button)

    def activate(self):
        self.updateList()

    def disable(self):
        self.installationList.enable(False)
        super(InstallTab, self).disable()

    def enable(self):
        self.installationList.enable(True)
        super(InstallTab, self).enable()

    def open_repo(self, sender):
        list = self.installationList.get()
        selections = self.installationList.getSelection()
        for selection in selections:
            cell = list[selection]
            webbrowser.open('http://github.com/%s' % cell['repository'])

    def install(self, sender):
        list = self.installationList.get()
        selections = self.installationList.getSelection()
        installable = []
        for selection in selections:
            installable.append(list[selection])

        ticks = len(installable) * 4
        self.progress = self.startProgress('Updating', ticks)

        for remote_cell in installable:
            remote = GithubRepo(remote_cell['repository'],
                                name=remote_cell['name'],
                                filename=remote_cell['filename'])
            extension_path = remote.download()
            Extension(path=extension_path).install()

        self.installationList.refresh()
        self.progress.close()
        self.update_buttons()

    def uninstall(self, sender):
        uninstallable = self._uninstallable()

        self.progress = self.startProgress('Updating', len(uninstallable))

        for extension in uninstallable:
            self.progress.update('Uninstalling %s...' % extension.name)
            Extension(path=extension.bundlePath()).uninstall()

        self.installationList.refresh()
        self.progress.close()
        self.update_buttons()

    def update_buttons(self, sender=None):
        self.update_install_button_label()
        self.update_uninstall_button_label()

    def update_uninstall_button_label(self, sender=None):
        self.uninstall_button._nsObject.setEnabled_(len(self._uninstallable()) > 0)

    def update_install_button_label(self, sender=None):
        selections = self.installationList.getSelection()
        self.install_button._nsObject.setEnabled_(selections)
        if len(selections) > 1:
            label = "Install %d Extensions" % len(selections)
        elif len(selections) is 1:
            label = "Install %d Extension" % len(selections)
        else:
            label = "Install Extensions"
        self.install_button.setTitle(label)

    def _uninstallable(self):
        available = self.installationList.get()
        selections = self.installationList.getSelection()
        uninstallable = []
        for selection in selections:
            name = available[selection]['filename'].split("/")[-1]
            extension = ExtensionBundle(name=name)
            if extension.bundleExists():
                uninstallable.append(extension)
        return uninstallable
