import os
import shutil
import plistlib
import errno
import requests

from mechanic import logger
from mechanic.lazy_property import lazy_property
from mechanic.version import Version
from mechanic.storage import Storage
from mechanic.event import evented

from .request import GithubRequest
from .tree import GithubTree
from .downloader import GithubDownloader


class GithubRepository(object):

    plist_url = "https://raw.github.com/%(repo)s/master/%(plist_path)s"

    @classmethod
    def concerning(cls, extension):
        return cls(extension.repository,
                   name=extension.name,
                   filename=extension.filename)

    def __init__(self, repo, name=None, filename=None):
        self.repo = repo
        self.filename = filename
        self.username, _ = repo.split('/', 1)
        self.name = name

    def read(self):
        """Return the version and location of remote extension."""
        try:
            plist_path = os.path.join(self.extension_path, 'info.plist')
            plist_url = self.plist_url % {'repo': self.repo, 'plist_path': plist_path}
            response = GithubRequest(plist_url).get()
            plist = plistlib.readPlistFromString(response.content)
            self.version = plist['version']
        except requests.exceptions.HTTPError:
            logger.warn("Couldn't get information about %s from %s" % (self.name, self.repo))
            self.version = '0.0.0'

    @evented('repository')
    def download(self):
        """Download remote version of extension."""
        return GithubDownloader(self.repo, self.filename).extract()

    @property
    def version(self):
        if hasattr(self, '_version'):
            return Version(self._version)
        else:
            self.read()
            return self.version

    @version.setter
    def version(self, value):
        self._version = value

    @lazy_property
    def extension_path(self):
        return self.tree.find(self.filename).get('path')

    @lazy_property
    def tree(self):
        return GithubTree(self.repo)
