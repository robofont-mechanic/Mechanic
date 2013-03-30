import os, shutil, errno, sys, re, plistlib, fnmatch
from glob import glob

import requests
from zipfile import ZipFile

from mojo.extensions import ExtensionBundle, getExtensionDefault, setExtensionDefault
from mechanic.helpers import Version

class Extension(object):
    """Facilitates loading the configuration from and updating extensions."""
    def __init__(self, name=None, path=None):
        self.config = {}
        self.configured = False
        self.bundle = ExtensionBundle(name=name, path=path)
        self.path = self.bundle.bundlePath()
        self.configure()

    def configure(self):
        """Set config attribute from info.plist contents."""
        self.configPath = os.path.join(self.path, 'info.plist')
        if(os.path.exists(self.configPath)):
            self.config = plistlib.readPlist(self.configPath)
            if 'repository' in self.config:
                self.configured = True
                self.remote = GithubRepo(self.config['repository'])
            
    def update(self, extension_path=None):
        """Download and install the latest version of the extension."""
        if extension_path is None:
            extension_path = self.remote.download()
        
        new_extension = Extension(path=extension_path)

        self.bundle.deinstall()
        new_extension.bundle.install()
        
    def is_current_version(self):
        """Return if extension is at curent version"""
        if not self.remote.version:
            self.remote.get()
        return Version(self.remote.version) <= Version(self.config['version'])

class GithubRepo(object):
    
    tags_url = "https://api.github.com/repos/%s/tags"

    def __init__(self, repo):
        self.repo = repo
        self.username, self.name = repo.split('/')
        self.version = None
        self.downloading = False
        self.chunk_count = None
        self.download_percentage = 0.0
        self.tmp_path = os.path.join("/", "tmp", "Mechanic", self.repo)
        
    def get(self):
        """Return the version and location of remote extension."""
        response = requests.get(self.tags_url % self.repo)
        response.raise_for_status()
        self.tags = response.json()
        try:
            self.tags.sort(key=lambda s: list(Version(s["name"])), reverse=True)
            self.data = self.tags[0]
            self.version = self.data['name']
        except:
            self.data = False
        return self.data
        
    def setup_download(self):
        """Clear extension tmp dir, open download stream and local file."""
        if not hasattr(self,'data'):
            self.get()
        self._flush_tmp_path()
        self.file = open(os.path.join(self.tmp_path, "%s.zip" % os.path.basename(self.data['zipball_url'])), "wb")
        self.stream = requests.get(self.data['zipball_url'], stream=True)
        self.stream_content = self.stream.iter_content(chunk_size=8192)
        self.content_length = self.stream.headers['content-length']
    
    def extract_file(self):
        """Extract downloaded zip file and return extension path."""
        zip_file = ZipFile(self.file.name)
        zip_file.extractall(self.tmp_path)
        os.remove(self.file.name)
        
        folder = os.path.join(self.tmp_path, os.listdir(self.tmp_path)[0])
        
        matches = []
        for root, dirnames, filenames in os.walk(self.tmp_path):
            for dirname in fnmatch.filter(dirnames, '*.roboFontExt'):
                matches.append(os.path.join(root, dirname))
                
        return matches[0]
    
    def download(self):
        """Download remote version of extension."""
        self.setup_download()
        for content in self.stream_content:
            self.file.write(content)
        self.file.close()
        return self.extract_file()

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
