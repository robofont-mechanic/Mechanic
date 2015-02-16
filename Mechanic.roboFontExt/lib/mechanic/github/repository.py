import requests

from mechanic import logger
from mechanic.lazy_property import lazy_property
from mechanic.version import Version
from mechanic.event import evented

from .request import GithubRequest
from .tree import GithubTree
from .downloader import GithubDownloader
from .plist import GithubPlist


class GithubRepository(object):

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

    @evented('repository')
    def download(self):
        """Download remote version of extension."""
        return GithubDownloader(self.repo, self.filename).extract()

    @lazy_property
    def version(self):
        try:
            return Version(GithubPlist(self.repo, self.extension_path)['version'])
        except requests.exceptions.HTTPError:
            logger.warn("Couldn't get information about %s from %s" % (self.name, self.repo))
            return Version('0.0.0')

    @lazy_property
    def tree(self):
        return GithubTree(self.repo)

    @lazy_property
    def extension_path(self):
        return self.tree.find(self.filename).get('path')
