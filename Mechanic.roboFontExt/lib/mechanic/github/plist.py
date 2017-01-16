import os
import plistlib
import xml

from mechanic.lazy_property import lazy_property

from .request import GithubRequest


PLIST_URL = "https://raw.github.com/%(repo)s/master/%(plist_path)s"


class GithubPlist(object):

    class MalformedPlistError(Exception): pass

    def __init__(self, repo, path):
        self.repo = repo
        self.plist_path = os.path.join(path, 'info.plist')

    def __getitem__(self, key):
        return self.data[key]

    @lazy_property
    def data(self):
        try:
            response = GithubRequest(self.plist_url).get()
            return plistlib.readPlistFromString(response.content)
        except xml.parsers.expat.ExpatError as e:
            raise GithubPlist.MalformedPlistError

    @lazy_property
    def plist_url(self):
        return PLIST_URL % {'repo': self.repo, 'plist_path': self.plist_path}
