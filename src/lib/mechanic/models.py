import os
import time

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

    def is_current_version(self):
        """Return if extension is at curent version"""
        # TODO: This requires too much knowledge about the GithubRepo class.
        # Accessing version should fetch the data internally.
        if not self.remote.version:
            self.remote.read()
        return Version(self.remote.version) <= Version(self.config['version'])

    def initialize_remote(self):
        if self.repository:
            return GithubRepo(self.repository,
                              name=self.name,
                              extension_path=self.extension_path)

    @property
    def may_update(self):
        ignore = Storage.get('ignore')
        return self.bundle.name not in ignore and self.is_configured

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
        return self.config.get('com.robofontmechanic.repository') or \
            self.config.get('repository')

    @property
    def extension_path(self):
        return self.config.get('extensionPath')


class Updates(object):

    @classmethod
    def last_checked(cls):
        return Storage.get('last_checked_at')

    @classmethod
    def checked_recently(cls):
        last_run = cls.last_checked()
        return last_run is not None and last_run > time.time() - (60 * 60)

    def __init__(self):
        self.unreachable = False

    def all(self, force=False, skip_patch_updates=False):
        if force or not self.__class__.checked_recently():
            updates = self._fetchUpdates()
        else:
            updates = self._getCached()

        if skip_patch_updates:
            updates = filter(self._filterPatchUpdates, updates)

        return updates

    def _fetchUpdates(self):
        updates = []
        extensions = [e for e in Extension.all() if e.may_update]
        try:
            updates = [e for e in extensions if not e.is_current_version()]
            self._setCached(updates)
            Storage.set('last_checked_at', time.time())
        except:
            self.unreachable = True
        return updates

    def _getCached(self):
        cache = Storage.get('cache')
        extensions = []
        for cached in cache.iteritems():
            extension = Extension(name=cached[0])
            if extension.is_configured:
                extension.remote.version = cached[1]
                extensions.append(extension)
        return extensions

    def _setCached(self, extensions):
        cache = {}
        for extension in extensions:
            cache[extension.bundle.name] = extension.remote.version
        Storage.set('cache', cache)

    def _filterPatchUpdates(self, update):
        local = Version(update.config.version)
        remote = Version(update.remote.version)
        return remote.major > local.major or remote.minor > remote.minor
