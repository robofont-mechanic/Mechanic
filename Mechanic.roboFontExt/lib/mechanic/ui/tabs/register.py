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
        self.name = TextField((20, 20, -20),
                              "Name",
                              placeholder="My Extension")

        self.filename = TextField((20, 60, -20),
                                  "Filename",
                                  placeholder="MyExtension.roboFontExt")

        self.repository = TextField((20, 100, -20),
                                    "Repository",
                                    placeholder="username/MyExtension")

        self.explanatory_text = TextBox((TextField.indent + 20, 135, -20, 50),
                                        self.explanation)

        self.import_button = Button((-250, -42, 80, 20),
                                    "Import",
                                    callback=self.get_extension)

        self.register_button = Button((-160, -42, 140, 20),
                                      "Register",
                                      callback=self.register)

    def activate(self):
        self.set_default_button(self.register_button)

    def get_extension(self, sender):
        getFile(fileTypes=['roboFontExt'],
                parentWindow=self.parent.w,
                resultCallback=self.import_extension)

    def import_extension(self, file):
        extension = Extension(path=file[0])
        if extension.bundle.bundleExists():
            self.name.set(extension.bundle.name)
            self.filename.set(extension.filename)
            self.repository.set(extension.repository)

    def register(self, sender):
        self.progress = self.start_progress('Sending to registry server...')
        try:
            registry = Registry(env.default_registry)
            response = registry.add(name=self.name.get(),
                                    filename=self.filename.get(),
                                    repository=self.repository.get())
            self.progress.close()
            response.raise_for_status()
            self.show_notification_sheet('%s was added.' % self.name.get())
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
        self.name.set('')
        self.filename.set('')
        self.repository.set('')
