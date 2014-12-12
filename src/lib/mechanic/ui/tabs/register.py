import os
import requests
from vanilla import *
from vanilla.dialogs import getFile

from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.ui.font import Font
from mechanic.ui.tabs.base import BaseTab


class RegisterTab(BaseTab):
    title = "Register"
    image = "toolbarScriptOpen"
    identifier = "register"

    tabSize = (500, 240)
    explanation = Font.string(text="Your name and the description of your extension will be based on the name/username and repository description on GitHub. Make sure these are set accordingly before registering your extension.", size=11)

    def setup(self):
        indent = 90

        self.content.extensionNameLabel = TextBox((0, 3, 80, 22),
                                                  "Name:",
                                                  alignment="right")

        self.content.extensionName = EditText((indent, 0, -0, 22),
                                              placeholder="My Extension")

        self.content.extensionFilenameLabel = TextBox((0, 43, 80, 22),
                                                      "Filename:",
                                                      alignment="right")

        self.content.extensionFilename = EditText((indent, 40, -0, 22),
                                                  placeholder="MyExtension.roboFontExt")

        self.content.extensionRepositoryLabel = TextBox((0, 83, 80, 22),
                                                        "Repository:",
                                                        alignment="right")

        self.content.extensionRepository = EditText((indent, 80, -0, 22),
                                                    placeholder="username/MyExtension")

        self.content.explanatoryText = TextBox((indent, 115, -0, 50),
                                               self.explanation)

        self.content.import_button = Button((-230, -22, 80, 20),
                                            "Import",
                                            callback=self.getExt)

        self.content.register_button = Button((-140, -22, 140, 20),
                                              "Register",
                                              callback=self.register)

    def activate(self):
        self.parent.w.setDefaultButton(self.content.register_button)

    def getExt(self, sender):
        getFile(fileTypes=['roboFontExt'], 
                parentWindow=self.parent.w, 
                resultCallback=self.importExt)

    def importExt(self, file):
        extension = Extension(path=file[0])
        if extension.bundle.bundleExists():
            self.content.extensionName.set(extension.bundle.name)
            self.content.extensionFilename.set(extension.filename)
            self.content.extensionRepository.set(extension.repository)

    def register(self, sender):
        self.progress = self.startProgress('Sending to registry server...')
        try:
            response = Registry().add(name=self.content.extensionName.get(),
                                      filename=self.content.extensionFilename.get(),
                                      repository=self.content.extensionRepository.get())
            self.progress.close()
            response.raise_for_status()
            self.showNotificationSheet('%s was added.' % self.extensionName.get())
            self.content.extensionName.set('')
            self.content.extensionFilename.set('')
            self.content.extensionRepository.set('')
        except requests.exceptions.HTTPError as e:
            errors = response.json()['error']
            if isinstance(errors, basestring): errors = [errors]
            errors = map(lambda e: '%s.' % e.capitalize(), errors)
            self.showNotificationSheet('\n'.join(errors), size=(300,len(errors)*22 + 60))
        except requests.exceptions.ConnectionError:
            self.progress.close()
            self.showConnectionErrorSheet()
