import time

from version import Version

from mechanic.storage import Storage
from mechanic.extension import Extension


class Updates(object):

    @classmethod
    def last_checked(cls):
        return Storage.get('last_checked_at') or 0

    @classmethod
    def checked_recently(cls):
        return cls.last_checked() > time.time() - (60 * 60)

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
        print "Mechanic: checking for updates..."

        updates = []
        extensions = [e for e in Extension.all() if e.may_update]
        try:
            updates = [e for e in extensions if not e.is_current_version]
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
