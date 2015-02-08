import time

from mechanic import env
from mechanic.version import Version
from mechanic.storage import Storage
from mechanic.extension import Extension


class Update(object):

    class ConnectionError(Exception): pass

    @classmethod
    def last_checked(cls):
        return Storage.get('last_checked_at') or 0

    @classmethod
    def checked_recently(cls):
        return cls.last_checked() > time.time() - env.updates_cache_interval

    @classmethod
    def all(cls, force=False, skip_patches=False):
        if force or not cls.checked_recently():
            updates = cls._fetch_updates()
        else:
            updates = cls._get_cached()

        if skip_patches:
            updates = filter(cls._filter_patch_updates, updates)

        return updates

    @classmethod
    def _fetch_updates(cls):
        print "Mechanic: checking for updates..."

        try:
            updates = [e for e in Extension.all() if e.should_update]
        except:
            raise Update.ConnectionError

        cls._set_cached(updates)
        Storage.set('last_checked_at', time.time())

        return updates

    @classmethod
    def _get_cached(cls):
        extensions = []
        for name, version in Storage.get('update_cache').items():
            extension = Extension(name=name)
            if extension.installed and extension.is_configured:
                extension.remote.version = version
                extensions.append(extension)
        return extensions

    @classmethod
    def _set_cached(cls, extensions):
        cache = {e.filename : str(e.remote.version) for e in extensions}
        Storage.set('update_cache', cache)

    @classmethod
    def _filter_patch_updates(cls, update):
        local = Version(update.config.version)
        remote = Version(update.remote.version)
        return remote.major > local.major or remote.minor > remote.minor
