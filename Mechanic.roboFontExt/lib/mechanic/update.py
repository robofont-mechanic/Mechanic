import time
import requests

from mechanic import env, logger
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
        logger.info("Fetching updates...")

        try:
            updates = [e for e in Extension.all() if e.should_update]
        except requests.ConnectionError:
            raise Update.ConnectionError

        cls._set_cached(updates)
        Storage.set('last_checked_at', time.time())

        return updates

    @classmethod
    def _get_cached(cls):
        logger.info("Fetching cached updates...")

        cache = Storage.get('update_cache').items()
        extensions = [Extension(name=name) for name, _ in cache]

        for extension in extensions:
            if extension.is_installed and extension.is_configured:
                extension.remote.version = cache[extension.name]['version']

        return extensions

    @classmethod
    def _set_cached(cls, extensions):
        cache = {e.filename : str(e.remote.version) for e in extensions}
        Storage.set('update_cache', cache)

    @classmethod
    def _filter_patch_updates(cls, extension):
        local = extension.version
        remote = extension.remote.version
        return remote.major > local.major or remote.minor > remote.minor
