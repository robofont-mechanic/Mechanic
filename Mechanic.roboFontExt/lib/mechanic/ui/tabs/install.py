from vanilla import *

from mechanic.threaded import ThreadedObject
from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.ui import progress
from mechanic.ui.tabs.base import BaseTab
from mechanic.ui.lists.installation import InstallationList


class InstallTab(BaseTab, ThreadedObject):
    title = "Install"
    image = "toolbarRun"
    identifier = "install"

    tab_size = (500, 400)

    def setup(self):
        self.list = InstallationList((20, 20, -20, -60),
                                     selectionCallback=self.update_buttons)

        self.uninstall_button = Button((-290, -42, 100, 20),
                                       "Uninstall",
                                       callback=self.uninstall)

        self.install_button = Button((-180, -42, 160, 20),
                                     "Install Extension",
                                     callback=self.in_thread.install)

        self.update_buttons()


    @progress.each('list.selected')
    @progress.tick('repositoryWillDownload',
                   'Downloading {repository.repo}')
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
        self.in_thread.update_list()

    def update_list(self):
        try:
            self.list.set(Registry.all())
            self.enable()
            self.set_default_button(self.install_button)
        except Registry.ConnectionError:
            self.disable("Couldn't connect to the registry server...")

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
        self.uninstall_button.enable(len(self.uninstallable) > 0)

    def update_install_button_label(self, sender=None):
        selections = self.list.getSelection()
        self.install_button.enable(selections)
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
        return [ext for ext in extensions if ext.is_installed]
