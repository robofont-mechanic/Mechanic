import os
import requests
from vanilla import *
from vanilla.dialogs import getFile

from mechanic import env
from mechanic.extension import Extension
from mechanic.registry import Registry
from mechanic.ui.fields.text_field import TextField
from mechanic.ui.text import Text
from mechanic.ui.tabs.base import BaseTab


class RegisterTab(BaseTab):
    title = "Register"
    image = "toolbarScriptOpen"
    identifier = "register"

    tab_size = (500, 240)
    explanation = Text.string(text="Your name and the description of your extension will be based on the name/username and repository description on GitHub. Make sure these are set accordingly before registering your extension.", size=11)

    def setup(self):
        self.content.name = TextField((0, 0),
                                      "Name",
                                      placeholder="My Extension")

        self.content.filename = TextField((0, 40),
                                          "Filename",
                                          placeholder="MyExtension.roboFontExt")

        self.content.repository = TextField((0, 80),
                                            "Repository",
                                            placeholder="username/MyExtension")

        self.content.explanatory_text = TextBox((TextField.indent, 115, -0, 50),
                                                self.explanation)

        self.content.import_button = Button((-230, -22, 80, 20),
                                            "Import",
                                            callback=self.get_extension)

        self.content.register_button = Button((-140, -22, 140, 20),
                                              "Register",
                                              callback=self.register)

    def activate(self):
        self.set_default_button(self.content.register_button)

    def get_extension(self, sender):
        getFile(fileTypes=['roboFontExt'],
                parentWindow=self.parent.w,
                resultCallback=self.import_extension)

    def import_extension(self, file):
        extension = Extension(path=file[0])
        if extension.bundle.bundleExists():
            self.content.name.set(extension.bundle.name)
            self.content.filename.set(extension.filename)
            self.content.repository.set(extension.repository)

    def register(self, sender):
        self.progress = self.start_progress('Sending to registry server...')
        try:
            registry = Registry(env.default_registry)
            response = registry.add(name=self.content.name.get(),
                                    filename=self.content.filename.get(),
                                    repository=self.content.repository.get())
            self.progress.close()
            response.raise_for_status()
            self.show_notification_sheet('%s was added.' % self.content.name.get())
            self.clear()
        except requests.exceptions.HTTPError as e:
            errors = response.json()['error']
            if isinstance(errors, basestring): errors = [errors]
            errors = map(lambda e: '%s.' % e.capitalize(), errors)
            self.show_notification_sheet('\n'.join(errors), size=(300,len(errors)*22 + 60))
        except requests.exceptions.ConnectionError:
            self.progress.close()
            self.show_connection_error_sheet()

    def clear(self):
        self.content.name.set('')
        self.content.filename.set('')
        self.content.repository.set('')
