import os

from mojo.extensions import ExtensionBundle
from version import Version

from mechanic.storage import Storage
from mechanic.repositories.github import GithubRepo
from mechanic.event import evented
from mechanic.configuration import Configuration


class Extension(object):
    """Facilitates loading the configuration from and updating extensions."""

    ticks_per_download = 4

    @classmethod
    def all(cls):
        return [cls(name=n) for n in ExtensionBundle.allExtensions()]

    def __init__(self, name=None, path=None):
        self.name = name
        self.bundle = ExtensionBundle(name=self.name, path=path)
        self.config = Configuration(self.config_path)
        self.remote = self.initialize_remote()

    @evented()
    def update(self, extension_path=None):
        """Download and install the latest version of the extension."""

        if extension_path is None:
            extension_path = self.remote.download()

        Extension(path=extension_path).install()

    @evented()
    def install(self):
        # TODO: Make this a noop if path isn't present
        self.bundle.install()

    @evented()
    def uninstall(self):
        self.bundle.deinstall()

    def initialize_remote(self):
        if self.repository:
            return GithubRepo(self.repository,
                              name=self.name,
                              extension_path=self.extension_path)

    @property
    def is_current_version(self):
        """Return if extension is at curent version"""
        # TODO: This requires too much knowledge about the GithubRepo class.
        # Accessing version should fetch the data internally.
        if not self.remote.version:
            self.remote.read()
        return Version(self.remote.version) <= self.version

    @property
    def may_update(self):
        return not self.is_ignored and self.is_configured

    @property
    def is_ignored(self):
        return self.bundle.name in Storage.get('ignore')

    @property
    def is_configured(self):
        return self.remote is not None

    @property
    def config_path(self):
        return os.path.join(self.path, 'info.plist')

    @property
    def path(self):
        return self.bundle.bundlePath()

    @property
    def repository(self):
        return self.config.namespaced('repository') or \
            self.config.deprecated('repository')

    @property
    def extension_path(self):
        return self.config.deprecated('extensionPath')

    @property
    def version(self):
        return Version(self.config['version'])

    @property
    def installed(self):
        return self.bundle.bundleExists()
