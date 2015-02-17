import os
import requests
import tempfile
import fnmatch

from zipfile import ZipFile


ZIP_URL = "https://github.com/%(repo)s/archive/master.zip"


class GithubDownloader(object):

    def __init__(self, repo, target):
        self.repo = repo
        self.target = target
        self.zip = self.download(self.zip_url)

    def download(self, url):
        tmp_dir = tempfile.mkdtemp()
        filepath = os.path.join(tmp_dir, os.path.basename(url))

        with open(filepath, "wb") as download:
            stream = requests.get(url, stream=True)
            chunks = stream.iter_content(chunk_size=8192)

            for content in chunks:
                self.download_chunk(download, content)

            stream.close()

        return filepath

    def download_chunk(self, file, content):
        file.write(content)

    def extract(self):
        """Extract downloaded zip file and return extension path."""
        destination = os.path.dirname(self.zip)

        ZipFile(self.zip).extractall(destination)

        os.remove(self.zip)

        match = '*%s' % self.target

        matches = []
        for root, dirnames, _ in os.walk(destination):
            for dirname in fnmatch.filter(dirnames, '*.roboFontExt'):
                matches.append(os.path.join(root, dirname))

        exact = fnmatch.filter(matches, match)
        return (exact and exact[0]) or None

    @property
    def zip_url(self):
        return ZIP_URL % {'repo': self.repo}
