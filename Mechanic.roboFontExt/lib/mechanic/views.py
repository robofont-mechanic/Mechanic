import json, webbrowser, os, re
from AppKit import *
from vanilla import *
from vanilla.dialogs import message
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.extensions import ExtensionBundle
from mechanic.helpers import *
from mechanic.models import Extension, GithubRepo

class UpdatesWindow(BaseWindowController):
    """Window to display extensions with newer remote versions."""
    window_title = "Extension Updates"
    title = Font.string(text="Updates are available for your RoboFont extensions.",style="bold")
    explanation = Font.string(text="The following extensions have updates available to download. If you don't want to install now, choose Extensions > Mechanic > Check for Updates when you're ready to install.",size=11)
    extImage = NSImage.imageNamed_("ExtensionIcon")
    no_updates_title = 'Mechanic'
    no_updates = 'All updateable extensions are up to date.'
    
    def __init__(self, quiet=False):
        self.updateables = []
        ignore = Storage.get('ignore')
        
        for name in ExtensionBundle.allExtentions():
            extension = Extension(name=name)
            if (not extension.bundle.name in ignore and
                    extension.configured and 
                    not extension.is_current_version()):
                self.updateables.append(extension)
        
        if len(self.updateables) > 0:
            self.w = Window((500,400),
                self.window_title,
                autosaveName="mechanicUpdatesWindow",
                minSize=(500,400))
            self.w.image = ImageView((15,15,80,80), scale='fit')
            if self.extImage:
                self.w.image.setImage(imageObject=self.extImage)
            self.w.title = TextBox((105,20,-20,20), self.title)
            self.w.explanation = TextBox((105,45,-20,50), self.explanation)
            
            self.w.updateableList = UpdatesList((20,110, -20, -50),
                self.updateables, editCallback=self.update_update_button_label)
            self.w.cancelButton = Button((-250,-35,80,20), "Not Now",
                callback=self.cancel)
            self.w.updateButton = Button((-160,-35,140,20), "Update",
                callback=self.update)
            self.update_update_button_label()
            self.w.setDefaultButton(self.w.updateButton)
            
            self.w.open()
        elif not quiet:
            message(self.no_updates_title, self.no_updates)
        else:
            print "%s: %s" % (self.no_updates_title, self.no_updates)

    def update_update_button_label(self, sender=None):
        rows = self.w.updateableList.get()
        count = 0
        for row in rows:
            if row['install']:
                count += 1
        self.w.updateButton._nsObject.setEnabled_(count is not 0)
        if count is 0:
            update_label = "Update"
        elif count is 1:
            update_label = "Install %d Update" % count
        else:
            update_label = "Install %d Updates" % count
        self.w.updateButton._nsObject.setTitle_(update_label)
        
    def cancel(self, sender):
        self.w.close()
        
    def update(self, sender):
        installable = []
        for extension in self.w.updateableList.get():
            if extension['install']:
                installable.append(extension['self'])
        
        ticks = len(installable) * 3
        self.progress = self.startProgress('Updating', ticks)

        for extension in installable:
            self.progress.update('Downloading %s...' % extension.bundle.name)
            try:
                extension.remote.setup_download()
                for content in extension.remote.stream_content:
                    extension.remote.file.write(content)
                extension.remote.file.close()
                self.progress.update('Extracting %s...' % extension.bundle.name)
                folder = extension.remote.extract_file()
                self.progress.update('Installing %s...' % extension.bundle.name)
                extension.update(folder)
            except:
                # ToDo: Make this report different errors
                print "Mechanic: Couldn't download %s" % extension.bundle.name
            
        self.progress.close()
        self.w.close()

class SettingsWindow(BaseWindowController):
    """Window to display extension settings."""
    window_title = "Mechanic Settings"
    checkbox_label = "Check for updates on startup"
    check_on_startup = Storage.get("check_on_startup")
    
    def __init__(self):
        self.configured = []
        for name in ExtensionBundle.allExtentions():
            extension = Extension(name=name)
            if extension.configured:
                self.configured.append(extension)
        
        self.w = Window((500,350),
            self.window_title,
            autosaveName="mechanicSettings")
        
        self.w.check_for_updates = CheckBox((20,20,-20,20),
            self.checkbox_label, value=self.check_on_startup)
        self.w.settingsList = SettingsList((20,60,-20,-50),
            self.configured)
        self.w.cancelButton = Button((-190,-35,80,20), "Cancel",
            callback=self.cancel)
        self.w.updateButton = Button((-100,-35,80,20), "Save",
            callback=self.update)
        self.w.setDefaultButton(self.w.updateButton)

        self.w.open()

    def update(self, sender):
        ignore = Storage.get("ignore")
        Storage.set("check_on_startup", 
                    bool(self.w.check_for_updates.get()))
        for row in self.w.settingsList.get():
            if not row["check_for_updates"]:
                ignore[row["name"]] = True
            elif row["name"] in ignore:
                del ignore[row["name"]]
        Storage.set('ignore', ignore)
        self.w.close()

    def cancel(self, sender):
        self.w.close()

class InstallationWindow(BaseWindowController):
    """Window to display installable extensions."""
    window_title = "Install Extensions"
    
    def __init__(self, registry='../registry.json'):
        registry_data = open(registry)
        registry = json.load(registry_data)
        
        self.w = Window((500,350),
            self.window_title,
            autosaveName="mechanicInstaller")
        
        self.w.installationList = InstallationList((20,20,-20,-50),
                                                   registry, 
                                                   selectionCallback=self.update_buttons,
                                                   allowsMultipleSelection=True)
        self.w.open_repo_button = Button((-330,-35,140,20), "Open Repository",
            callback=self.open_repo)
        self.w.install_button = Button((-180,-35,160,20), "Install Extension",
            callback=self.install)
        self.update_install_button_label()
        self.w.setDefaultButton(self.w.install_button)
        
        self.w.open()
            
    def open_repo(self, sender):
        list = self.w.installationList.get()
        selections = self.w.installationList.getSelection()
        for selection in selections:
            cell = list[selection]
            webbrowser.open('http://github.com/%s' % cell['repository'])
        
    def install(self, sender):
        list = self.w.installationList.get()
        selections = self.w.installationList.getSelection()
        installable = []
        for selection in selections:
            installable.append(list[selection])
            
        ticks = len(installable) * 4
        self.progress = self.startProgress('Updating', ticks)

        for remote_cell in installable:
            remote = GithubRepo(remote_cell['repository'], name=remote_cell['name'])
            try:
                self.progress.update('Getting data from %s...' % remote_cell['repository'])
                remote.get()
                self.progress.update('Downloading %s...' % remote_cell['name'])
                remote.setup_download()
                for content in remote.stream_content:
                    remote.file.write(content)
                remote.file.close()
                self.progress.update('Extracting %s...' % remote_cell['name'])
                extension_path = remote.extract_file()
                self.progress.update('Installing %s...' % remote_cell['name'])

                new_extension = Extension(path=extension_path)
                new_extension.bundle.install()
            except:
                # ToDo: Make this report different errors
                print "Mechanic: Couldn't download %s" % remote_cell['name']
            
        self.progress.close()


    def update_buttons(self, sender=None):
        self.update_install_button_label()
        self.update_repo_button_label()
        
    def update_repo_button_label(self, sender=None):
        selections = self.w.installationList.getSelection()
        self.w.open_repo_button._nsObject.setEnabled_(selections)
        if len(selections) > 1:
            label = "Open Repositories"
        else:
            label = "Open Repository"
        self.w.open_repo_button._nsObject.setTitle_(label)
        
    def update_install_button_label(self, sender=None):
        selections = self.w.installationList.getSelection()
        self.w.install_button._nsObject.setEnabled_(selections)
        if len(selections) > 1:
            label = "Install %d Extensions" % len(selections)
        elif len(selections) is 1:
            label = "Install %d Extension" % len(selections)
        else:
            label = "Install Extensions"
        self.w.install_button._nsObject.setTitle_(label)
    