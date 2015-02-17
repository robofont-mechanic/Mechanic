import os
import shutil

from mojo.extensions import ExtensionBundle

from mechanic.version import Version
from mechanic.storage import Storage
from mechanic.github.repository import GithubRepository
from mechanic.event import evented
from mechanic.configuration import Configuration
from mechanic.lazy_property import lazy_property


class Extension(object):
    """Facilitates loading the configuration from and updating extensions."""

    ticks_per_download = 4

    @classmethod
    def all(cls):
        return [cls(name=n) for n in ExtensionBundle.allExtensions()]

    @classmethod
    def install_remote(cls, repository, name, filename):
        remote = GithubRepository(repository, name=name, filename=filename)
        path = remote.download()
        extension = cls(path=path).install()
        shutil.rmtree(path) # TODO: removing the tree should happen after download somehow
        return extension

    def __init__(self, name=None, path=None):
        self.name = name
        self.bundle = ExtensionBundle(name=self.name, path=path)
        self.config = Configuration(self.config_path)

    @evented()
    def update(self, path=None):
        """Download and install the latest version of the extension."""

        if path is None:
            path = self.remote.download()

        Extension(path=path).install()

    @evented()
    def install(self):
        self.bundle.install()

    @evented()
    def uninstall(self):
        self.bundle.deinstall()

    @lazy_property
    def remote(self):
        return GithubRepository.concerning(self)

    @property
    def is_current_version(self):
        """Return if extension is at curent version"""
        return self.remote.version <= self.version

    @property
    def may_update(self):
        return not self.is_ignored and self.is_configured

    @property
    def should_update(self):
        return self.may_update and not self.is_current_version

    @property
    def is_ignored(self):
        return self.bundle.name in Storage.get('ignore')

    @property
    def is_configured(self):
        return self.repository is not None

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
    def version(self):
        return Version(self.config['version'])

    @property
    def installed(self):
        return self.bundle.bundleExists()

    @property
    def filename(self):
        return os.path.basename(self.bundle.bundlePath())
