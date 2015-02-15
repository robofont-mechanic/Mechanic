import os
import shutil
import plistlib
import fnmatch
import errno
import requests

from zipfile import ZipFile

from mechanic import logger
from mechanic.lazy_property import lazy_property
from mechanic.version import Version
from mechanic.storage import Storage
from mechanic.event import evented

from .request import GithubRequest
from .tree import GithubTree


class GithubRepository(object):

    zip_url = "https://github.com/%(repo)s/archive/master.zip"
    plist_url = "https://raw.github.com/%(repo)s/master/%(plist_path)s"

    @classmethod
    def concerning(cls, extension):
        return cls(extension.repository,
                   name=extension.name,
                   filename=extension.filename)

    def __init__(self, repo, name=None, filename=None):
        self.repo = repo
        self.filename = filename
        self.username, self.name = repo.split('/')
        if name is not None:
            self.name = name

    @evented('repository')
    def read(self):
        """Return the version and location of remote extension."""
        try:
            plist_path = os.path.join(self.extension_path, 'info.plist')
            plist_url = self.plist_url % {'repo': self.repo, 'plist_path': plist_path}
            response = GithubRequest(plist_url).get()
            plist = plistlib.readPlistFromString(response.content)
            self.version = plist['version']
            self.zip = self.zip_url % {'repo': self.repo}
        except requests.exceptions.HTTPError:
            logger.info("Couldn't get information about %s from %s" % (self.name, self.repo))
            self.version = '0.0.0'

    def setup_download(self):
        """Clear extension tmp dir, open download stream and local file."""
        self.read()
        self._flush_tmp_path()
        filepath = os.path.join(self.tmp_path, os.path.basename(self.zip))
        self.file = open(filepath, "wb")
        self.stream = requests.get(self.zip, stream=True)
        self.stream_content = self.stream.iter_content(chunk_size=8192)
        self.content_length = self.stream.headers['content-length']

    @evented('repository')
    def extract_download(self):
        """Extract downloaded zip file and return extension path."""
        ZipFile(self.file.name).extractall(self.tmp_path)
        os.remove(self.file.name)

        folder = os.path.join(self.tmp_path, os.listdir(self.tmp_path)[0])

        match = '*%s' % self.filename

        # TODO: Make this use a generator
        matches = []
        for root, dirnames, _ in os.walk(self.tmp_path):
            for dirname in fnmatch.filter(dirnames, '*.roboFontExt'):
                matches.append(os.path.join(root, dirname))

        exact = fnmatch.filter(matches, match)
        path = (exact and exact[0]) or None

        return path

    @evented('repository')
    def download(self):
        """Download remote version of extension."""

        try:
            self.setup_download()
            for content in self.stream_content:
                self.download_chunk(content)
        finally:
            self.stream.close()
            self.file.close()

        return self.extract_download()

    @evented('repository', 'downloadChunk')
    def download_chunk(self, content):
        self.file.write(content)

    @property
    def tmp_path(self):
        return os.path.join("/", "tmp", "Mechanic", self.repo)

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

    def _flush_tmp_path(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
        mkdir_p(self.tmp_path)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
