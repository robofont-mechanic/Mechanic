import os
import shutil
import plistlib
import fnmatch
import errno
import requests

from mojo.events import postEvent
from zipfile import ZipFile
from version import Version

from mechanic.storage import Storage
from mechanic.event import evented


class GithubRepo(object):

    tags_url = "https://api.github.com/repos/%(repo)s/tags"
    zip_url = "https://github.com/%(repo)s/archive/master.zip"
    plist_url = "https://raw.github.com/%(repo)s/master/%(plist_path)s"

    def __init__(self, repo, name=None, extension_path=None, filename=None):
        self.repo = repo
        self.extension_path = extension_path
        self.filename = filename
        self.username, self.name = repo.split('/')
        if name is not None:
            self.name = name
        self.version = None

    @evented('repository', 'read')
    def read(self):
        """Return the version and location of remote extension."""

        if not hasattr(self, 'data'):
            try:
                if self.extension_path:
                    plist_path = os.path.join(self.extension_path, 'info.plist')
                    plist_url = self.plist_url % {'repo': self.repo, 'plist_path': plist_path}
                    response = GithubRequest(plist_url).get()
                    plist = plistlib.readPlistFromString(response.content)
                    self.version = plist['version']
                    self.zip = self.zip_url % {'repo': self.repo}
                elif self._get_tags():
                    self.tags.sort(key=lambda s: Version(s["name"]),
                                   reverse=True)
                    self.zip = self.tags[0]['zipball_url']
                    self.version = self.tags[0]['name']
                else:
                    self.zip = self.zip_url % {'repo': self.repo}
            except requests.exceptions.HTTPError:
                print "Couldn't get information about %s from %s" % (self.name, self.repo)
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

    @evented('repository', 'extractDownload')
    def extract_file(self):
        """Extract downloaded zip file and return extension path."""
        zip_file = ZipFile(self.file.name)
        zip_file.extractall(self.tmp_path)
        os.remove(self.file.name)

        folder = os.path.join(self.tmp_path, os.listdir(self.tmp_path)[0])

        if self.extension_path:
            path = os.path.join(folder, self.extension_path)
        else: 
            if self.filename:
                match = '*%s' % self.filename
            else:
                match = '*%s.roboFontExt' % self.name

            # TODO: Make this use a generator
            matches = []
            for root, dirnames, filenames in os.walk(self.tmp_path):
                for dirname in fnmatch.filter(dirnames, '*.roboFontExt'):
                    matches.append(os.path.join(root, dirname))

            exact = fnmatch.filter(matches, match)
            path = (exact and exact[0]) or None

        return path

    @evented('repository', 'download')
    def download(self):
        """Download remote version of extension."""

        self.setup_download()

        try:
            for content in self.stream_content:
                self.download_chunk(content)
        finally:
            self.stream.close()
            self.file.close()

        return self.extract_file()

    @evented('repository', 'downloadChunk')
    def download_chunk(self, content):
        self.file.write(content)

    @property
    def tmp_path(self):
        return os.path.join("/", "tmp", "Mechanic", self.repo)

    def _get_tags(self):
        url = self.tags_url % {'repo': self.repo}
        response = GithubRequest(url).get()
        self.tags = response.json()
        return self.tags

    def _flush_tmp_path(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
        mkdir_p(self.tmp_path)


class GithubRequest(object):

    __cache = {}

    def __init__(self, url):
        self.url = url

    def get(self):
        return self.cache_response(self.url, self.get_cached(self.url))

    def get_cached(self, url):
        cached_response = self.cache.get(url, None)
        if cached_response is not None:
            etag = self.get_etag(cached_response)
            response = requests.get(url, headers={'If-None-Match': etag})
            if response.status_code is 304:
                response = cached_response
        else:
            response = requests.get(url)
        response.raise_for_status()
        return response

    def cache_response(self, url, response):
        if self.get_etag(response):
            self.cache[url] = response
        return response

    def get_etag(self, response):
        return response.headers['ETag']

    @property
    def cache(self):
        return self.__class__.__cache


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
