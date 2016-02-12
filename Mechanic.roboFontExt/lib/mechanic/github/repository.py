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

    def __init__(self, repo, filename=None):
        self.repo = repo
        self.filename = filename

    @evented('repository')
    def download(self):
        """Download remote version of extension."""
        return GithubDownloader(self.repo, self.filename).extract()

    @lazy_property
    def version(self):
        try:
            return Version(GithubPlist(self.repo, self.extension_path)['version'])
        except requests.exceptions.HTTPError as e:
            logger.warn("Couldn't get version information from %s\n\tHTTP status: %d\n\tresponse: %s",
                        self.repo,
                        e.response.status_code,
                        e.response.text)
            return Version('0.0.0')
        except AttributeError:
            logger.warn("(Probably) Couldn't fetch the GitHub file tree for %s", self.repo)
            return Version('0.0.0')

    @lazy_property
    def tree(self):
        return GithubTree(self.repo)

    @lazy_property
    def extension_path(self):
        return self.tree.find(self.filename).get('path')
