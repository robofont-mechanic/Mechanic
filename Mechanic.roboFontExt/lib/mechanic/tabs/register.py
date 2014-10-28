import os
import requests
from vanilla import *
from vanilla.dialogs import getFile
from mojo.extensions import ExtensionBundle

from mechanic.lists import *
from mechanic.models import Extension
from mechanic.registry import Registry
from mechanic.font import Font
from mechanic.tabs.base import BaseTab


class RegisterTab(BaseTab):
    title = "Register"
    image = "toolbarScriptOpen"
    identifier = "register"
    
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
            response = Registry().add(name=self.extensionName.get(),
                                      filename=self.extensionFilename.get(),
                                      repository=self.extensionRepository.get())
            self.progress.close()
            response.raise_for_status()
            self.showNotificationSheet('%s was added.' % self.extensionName.get())
            self.extensionName.set('')
            self.extensionFilename.set('')
            self.extensionRepository.set('')
        except requests.exceptions.HTTPError as e:
            errors = response.json()['error']
            if isinstance(errors, basestring): errors = [errors]
            errors = map(lambda e: '%s.' % e.capitalize(), errors)
            self.showNotificationSheet('\n'.join(errors), size=(300,len(errors)*22 + 60))
        except requests.exceptions.ConnectionError:
            self.progress.close()
            self.showConnectionErrorSheet()
