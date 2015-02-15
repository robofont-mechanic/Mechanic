import os
import shutil
import plistlib
import fnmatch
import errno
import requests
import tempfile

from zipfile import ZipFile

from mechanic import logger
from mechanic.lazy_property import lazy_property
from mechanic.version import Version
from mechanic.storage import Storage
from mechanic.event import evented

from .request import GithubRequest
from .tree import GithubTree


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

    @evented('repository')
    def read(self):
        """Return the version and location of remote extension."""
        try:
            plist_path = os.path.join(self.extension_path, 'info.plist')
            plist_url = self.plist_url % {'repo': self.repo, 'plist_path': plist_path}
            response = GithubRequest(plist_url).get()
            plist = plistlib.readPlistFromString(response.content)
            self.version = plist['version']
        except requests.exceptions.HTTPError:
            logger.info("Couldn't get information about %s from %s" % (self.name, self.repo))
            self.version = '0.0.0'

    @evented('repository')
    def extract_download(self, filepath, destination):
        """Extract downloaded zip file and return extension path."""

        ZipFile(filepath).extractall(destination)

        os.remove(filepath)

        match = '*%s' % self.filename

        # TODO: Make this use a generator
        matches = []
        for root, dirnames, _ in os.walk(destination):
            for dirname in fnmatch.filter(dirnames, '*.roboFontExt'):
                matches.append(os.path.join(root, dirname))

        exact = fnmatch.filter(matches, match)
        return (exact and exact[0]) or None

    @evented('repository')
    def download(self):
        """Download remote version of extension."""
        tmp_dir = tempfile.mkdtemp()

        try:
            zip_path = os.path.join(tmp_dir, os.path.basename(self.zip_url))
            zip_file = open(zip_path, "wb")
            stream = requests.get(self.zip_url, stream=True)
            chunks = stream.iter_content(chunk_size=8192)

            for content in chunks:
                self.download_chunk(zip_file, content)
        finally:
            try:
                shutil.rmtree(tmp_dir)
                zip_file.close()
                stream.close()
            except: pass

        return self.extract_download(zip_file.name, tmp_dir)

    @evented('repository', 'downloadChunk')
    def download_chunk(self, file, content):
        return file.write(content)

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

    @property
    def zip_url(self):
        return "https://github.com/%(repo)s/archive/master.zip" % {
            'repo': self.repo
        }

    @lazy_property
    def extension_path(self):
        return self.tree.find(self.filename).get('path')

    @lazy_property
    def tree(self):
        return GithubTree(self.repo)
