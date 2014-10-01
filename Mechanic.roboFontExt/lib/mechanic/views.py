import json, webbrowser, os, re, time, plistlib, requests
from AppKit import *
from vanilla import *
from vanilla.dialogs import message, getFile
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.extensions import ExtensionBundle
from mechanic.helpers import *
from mechanic.models import Extension, GithubRepo, Registry, Updates

class MechanicWindow(BaseWindowController):
    """Window to display all Mechanic stuff"""
    toolbarImagesMap = {
                        "Install" : "toolbarRun",
                        "Update" : "toolbarScriptReload",
                        "Register" : "toolbarScriptOpen",
                        "Settings" : "prefToolbarMisc",
                       }
    items = ["Install", "Update", "Register", "Settings"]
    
    def __init__(self, active="Install"):
        self.w = Window((500,300),
                        autosaveName="mechanicWindow",
                        title="Mechanic")

        self.addToolbar()
        self.addTabs()
        self.setActivePane(active)
        
        self.w.open()

    def addToolbar(self):
        toolbarItems = []
        for index, value in enumerate(self.items):
            toolbarItem = dict(itemIdentifier=value,
                               label=value,
                               callback=self.toolbarSelect,
                               imageNamed=self.toolbarImagesMap[value],
                               selectable=True
                               )
            toolbarItems.append(toolbarItem)

        self.w.addToolbar(toolbarIdentifier="mechanicToolbar", toolbarItems=toolbarItems, addStandardItems=False)
    
    def setActivePane(self, pane):
        current_index = self.w.tabs.get()
        index = self.items.index(pane)
        if not self.w.isVisible():
            self.w.getNSWindow().toolbar().setSelectedItemIdentifier_(pane)
        self.w.tabs.set(index)
        self.w.tabs[current_index].view.deactivate()
        self.w.tabs[index].view.setWindowSize()
        self.w.tabs[index].view.activate()
        name = self.items[index]

    def toolbarSelect(self, sender):
        self.setActivePane(sender.itemIdentifier())
        
    def addTabs(self):
        self.w.tabs = Tabs((0, 0, -0, -0), self.items, showTabs=False)        
        self.install = self.w.tabs[0]
        self.update = self.w.tabs[1]
        self.register = self.w.tabs[2]
        self.settings = self.w.tabs[3]
        self.install.view = InstallTab((0,0,-0,-0), self)
        self.update.view = UpdatesTab((0,0,-0,-0), self)
        self.register.view = RegisterTab((0,0,-0,-0), self)
        self.settings.view = SettingsTab((0,0,-0,-0), self)

class UpdateNotificationWindow(BaseWindowController):
    window_title = "Extension Updates"
    explanation = Font.string(text="If you don't want to install now, choose Extensions > Mechanic > Updates when you're ready to install.",size=11)
    extImage = NSImage.imageNamed_("ExtensionIcon")
    no_updates_title = 'Mechanic'
    no_updates = 'All updateable extensions are up to date.'

    def __init__(self, force=False):
        self.updater = Updates()
        self.updates = self.updater.all(force)
        if bool(Storage.get('ignore_patch_updates')):
            self.updates = filter(self._filterPatchUpdates, self.updates)
            
        if self.updater.unreachable:
            print "%s: Couldn't connect to the internet" % self.no_updates_title
            return
            
        if len(self.updates) > 0:
            self.w = Window((520,130),
                            self.window_title,
                            autosaveName="mechanicUpdatesWindow")
            
            self.w.image = ImageView((15,15,80,80), scale='fit')
            if self.extImage:
                self.w.image.setImage(imageObject=self.extImage)
            
            self.w.title = TextBox((105,20,-20,20), self.title(len(self.updates)))
            self.w.explanation = TextBox((105,45,-20,50), self.explanation)
            
            self.w.updateButton = Button((-150,-40,130,20), "Install Updates",
                                         callback=self.update)
            self.w.cancelButton = Button((-255,-40,90,20), "Not Now",
                                         callback=self.cancel)
            self.w.showDetailsButton = Button((105,-40,110,20), "Show Details",
                                         callback=self.showDetails)
            self.w.setDefaultButton(self.w.updateButton)
            
            self.w.open()
        else:
            print "%s: %s" % (self.no_updates_title, self.no_updates)
    
    def title(self, len):
        return Font.string(text="Updates are available for %d of your extensions." % len,style="bold")
    
    def cancel(self, sender):
        self.w.close()
        
    def update(self, sender):            
        ticks = len(self.updates) * 4
        self.progress = self.startProgress('Updating', ticks)

        for extension in self.updates:
            try:
                self.progress.update('Getting %s...' % extension.config.repository)
                extension.remote.get()
                self.progress.update('Downloading %s...' % extension.bundle.name)
                extension.remote.setup_download()
                for content in extension.remote.stream_content:
                    extension.remote.file.write(content)
                extension.remote.file.close()
                self.progress.update('Extracting %s...' % extension.bundle.name)
                extension_path = extension.remote.extract_file()
                self.progress.update('Installing %s...' % extension.bundle.name)

                new_extension = Extension(path=extension_path)
                new_extension.bundle.install()
            except:
                # ToDo: Make this report different errors
                print "Mechanic: Couldn't download %s" % extension.bundle.name
            
        self.progress.close()
        
    def showDetails(self, sender):
        self.w.close()
        MechanicWindow("Update")
        
    def _filterPatchUpdates(self, update):
        local = Version(update.config.version)
        remote = Version(update.remote.version)
        return remote.major > local.major or remote.minor > remote.minor

class MechanicTab(VanillaBaseObject):
    nsViewClass = NSView
    disabledText = "Couldn't connect to the Internet..."
    tabSize = (500, 300)
    
    def __init__(self, posSize, parent=None):
        self._setupView(self.nsViewClass, posSize)
        self.parent = parent
        self.setup()
        
    def setup(self):
        pass
        
    def activate(self):
        pass
        
    def deactivate(self):
        pass
        
    def setWindowSize(self):
        self.parent.w.resize(self.tabSize[0], self.tabSize[1], False)
        
    def disable(self):
        if not hasattr(self, 'disabledOverlay'):
            colorTile = NSImage.alloc().initWithSize_((10, 10))
            colorTile.lockFocus()
            color = NSColor.colorWithCalibratedWhite_alpha_(0, 0.65)
            color.set()
            NSRectFillUsingOperation(((0, 0), (10, 10)), NSCompositeSourceOver)
            colorTile.unlockFocus()
        
            self.disabledOverlay = Group((0,0,-0,-0))
            self.disabledOverlay.background = ImageView((0, 0, 0, 0), scale="fit")
            self.disabledOverlay.background.setImage(imageObject=colorTile)
        
            disabledText = Font.string(self.disabledText)
            self.disabledOverlay.disabledText = TextBox((0,120,-0,-0), self.disabledText, alignment="center")
            self.disabledOverlay.disabledText._nsObject.setTextColor_(NSColor.whiteColor())
            
    def enable(self):
        if hasattr(self, 'disabledOverlay'):
            self.disabledOverlay._nsObject.removeFromSuperview()
        
    def startProgress(self, *args, **kwargs):
        return self.parent.startProgress(*args, **kwargs)

    def closeNotificationSheet(self, sender):
        self.parent.w.notification.close()
        
    def showNotificationSheet(self, text, size=(300, 80)):
        self.parent.w.notification = Sheet(size, self.parent.w)
        self.parent.w.notification.text = TextBox((15, 15, -50, -15), text)
        self.parent.w.notification.closeButton = Button((-115,-37,100,22), 'Close', callback=self.closeNotificationSheet)
        self.parent.w.notification.setDefaultButton(self.parent.w.notification.closeButton)
        self.parent.w.notification.open()
    
    def showConnectionErrorSheet(self):
        self.showNotificationSheet(self.disabledText)

class UpdatesTab(MechanicTab):

    def setup(self):
        self.addList()
        self.addUpdatedAt()
        self.addUpdateButton()

    def activate(self):
        self.parent.w.setDefaultButton(self.updateButton)
        self.updateList()

    def addList(self): 
        posSize = (20,20,-20,-50)           
        self.updateableList = UpdatesList(posSize,
                                          [], 
                                          editCallback=self.updateUpdateButtonLabel)
    
    def updateList(self, force=False):
        updater = Updates()
        updates = updater.all(force)
        if not updater.unreachable:
            self.updateableList.set(updates)
            self.updateUpdatedAt()            
    
    def addUpdatedAt(self):
        self.updatedAt = TextBox((20,-31,-20,20), 
                         "",
                         sizeStyle="small")
        self.updateUpdatedAt()

    def updateUpdatedAt(self):
        updated = Updates().updatedAt()
        if updated:
            self.updatedAt.set("Last checked: %s" % time.strftime('%d %b %Y, %H:%M', time.localtime(updated)))
        else:
            self.updatedAt.set('')

    def addUpdateButton(self):
        self.updateButton = Button((-160,-35,140,20), "Update",
                            callback=self.update)
        self.updateUpdateButtonLabel()

    def updateUpdateButtonLabel(self, sender=None):
        rows = self.updateableList.get()
        count = 0
        for row in rows:
            if row['install']:
                count += 1
        self.updateButton._nsObject.setEnabled_(count is not 0)
        if count is 0:
            update_label = "Update"
        elif count is 1:
            update_label = "Install %d Update" % count
        else:
            update_label = "Install %d Updates" % count
        self.updateButton._nsObject.setTitle_(update_label)
                
    def update(self, sender):
        installable = []
        for extension in self.updateableList.get():
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
        
        self.updateList(True)
        self.progress.close()

class SettingsTab(MechanicTab):
    updates_label = "Check for updates on startup"
    minor_updates_label = "Ignore patch updates on startup"
    check_on_startup = Storage.get("check_on_startup")

    def setup(self):                
        self.addList()
        self.checkForUpdates = CheckBox((20,15,-20,20),
                                          self.updates_label,
                                          value=Storage.get("check_on_startup"),
                                          callback=self.saveCheckForUpdates)
        self.ignorePatchUpdates = CheckBox((20,40,-20,20),
                                             self.minor_updates_label,
                                             value=Storage.get("ignore_patch_updates"),
                                             callback=self.saveIgnorePatchUpdates)

    def addList(self):
        self.configured = []
        for name in ExtensionBundle.allExtensions():
            extension = Extension(name=name)
            if extension.configured:
                self.configured.append(extension)

        self.settingsList = SettingsList((20,75,-20,-20),
                                         self.configured,
                                         editCallback=self.update)

    def saveCheckForUpdates(self, sender):
        Storage.set("check_on_startup", 
            bool(self.checkForUpdates.get()))

    def saveIgnorePatchUpdates(self, sender):
        Storage.set("ignore_patch_updates", 
            bool(self.ignorePatchUpdates.get()))

    def update(self, sender):
        ignore = Storage.get("ignore")
        for row in self.settingsList.get():
            if not row["check_for_updates"]:
                ignore[row["name"]] = True
            elif row["name"] in ignore:
                del ignore[row["name"]]
        Storage.set('ignore', ignore)

class InstallTab(MechanicTab):
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
                                name = remote_cell['name'],
                                filename = remote_cell['filename'])
            try:
                self.progress.update('Getting %s...' % remote_cell['repository'])
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
            
        self.installationList.refresh()
        self.progress.close()
        self.update_buttons()
        
    def uninstall(self, sender):
        uninstallable = self._uninstallable()
    
        self.progress = self.startProgress('Updating', len(uninstallable))

        for extension in uninstallable:
            self.progress.update('Uninstalling %s...' % extension.name)
            extension.deinstall()

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
        self.install_button._nsObject.setTitle_(label)
        
    def _uninstallable(self):
        list = self.installationList.get()
        selections = self.installationList.getSelection()
        uninstallable = []
        for selection in selections:
            extension = ExtensionBundle(name=list[selection]['filename'].split("/")[-1])
            if extension.bundleExists():
                uninstallable.append(extension)
        return uninstallable

class RegisterTab(MechanicTab):
    tabSize = (500, 225)
    explanation = Font.string(text="Your name and the description of your extension will be based on the name/username and repository description on GitHub. Make sure these are set accordingly before registering your extension.", size=11)
    
    def setup(self):
        indent = 105
        
        self.extensionNameLabel = TextBox((15,18,80,22), "Name:", alignment="right")
        self.extensionName = EditText((indent,15,-20,22), placeholder="My Extension")

        self.extensionFilenameLabel = TextBox((15,58,80,22), "Filename:", alignment="right")
        self.extensionFilename = EditText((indent,55,-20,22), placeholder="MyExtension.roboFontExt")

        self.extensionRepositoryLabel = TextBox((15,98,80,22), "Repository:", alignment="right")
        self.extensionRepository = EditText((indent,95,-20,22), placeholder="username/MyExtension")
        
        self.explanatoryText = TextBox((105,130,-20,50), self.explanation)
                
        self.importButton = Button((-250,-35,80,20), "Import",
                                   callback=self.getExt)
        self.registerButton = Button((-160,-35,140,20), "Register",
                                     callback=self.register)

    def activate(self):
        self.parent.w.setDefaultButton(self.registerButton)    

    def getExt(self, sender):
        getFile(fileTypes=['roboFontExt'], 
                parentWindow=self.parent.w, 
                resultCallback=self.importExt)
        
    def importExt(self, file):
        extension = Extension(path=file[0])
        if extension.bundle.bundleExists():
            self.extensionName.set(extension.bundle.name)
            self.extensionFilename.set(os.path.basename(extension.path))
            self.extensionRepository.set(extension.config.repository)
        
    def register(self, sender):
        self.progress = self.startProgress('Sending to registry server...')
        try:
            response = Registry().add({
                                       'name': self.extensionName.get(),
                                       'filename': self.extensionFilename.get(),
                                       'repository': self.extensionRepository.get()
                                      })
            self.progress.close()
            response.raise_for_status()
            self.showNotificationSheet('%s was added.' % self.extensionName.get())
            self.extensionName.set('')
            self.extensionFilename.set('')
            self.extensionRepository.set('')
        except requests.exceptions.HTTPError, e:
            errors = response.json()['error']
            if isinstance(errors, basestring): errors = [errors]
            errors = map(lambda e: '%s.' % e.capitalize(), errors)
            self.showNotificationSheet('\n'.join(errors), size=(300,len(errors)*22 + 60))
        except requests.exceptions.ConnectionError:
            self.progress.close()
            self.showConnectionErrorSheet()
