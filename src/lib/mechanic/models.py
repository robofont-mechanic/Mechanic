import os, shutil, errno, sys, re, plistlib, fnmatch, time, json
from glob import glob

import requests
from zipfile import ZipFile

from mojo.events import postEvent
from mojo.extensions import ExtensionBundle
from mechanic.helpers import Version, Storage

class Extension(object):
    """Facilitates loading the configuration from and updating extensions."""
    
    ticks_per_download = 4
    
    def __init__(self, name=None, path=None):
        self.name = name
        self.bundle = ExtensionBundle(name=self.name, path=path)
        self.path = self.bundle.bundlePath()
        self.config = None
        self.remote = None
        self.configure_remote()

    def configure_remote(self):
        """Set config attribute from info.plist contents."""
        self.config = self.read_config()
        if self.config is not None:
            self.remote = self.initialize_remote()
            
    def update(self, extension_path=None):
        """Download and install the latest version of the extension."""
        
        postEvent('extensionWillUpdate', extension=new_extension)
        
        if extension_path is None:
            extension_path = self.remote.download()

        Extension(path=extension_path).install()

        postEvent('extensionDidUpdate', extension=new_extension)
    
    def install(self):
        # TODO: Make this a noop if path isn't present
        postEvent('extensionWillInstall', extension=new_extension)
        
        self.uninstall_duplicates()
        self.bundle.install()
        
        postEvent('extensionDidInstall', extension=new_extension)

    def uninstall_duplicates(self):
        existing_extension = ExtensionBundle(name=self.name)
        if existing_extension.bundleExists():
            existing_extension.bundle.deinstall()

    def is_current_version(self):
        """Return if extension is at curent version"""
        if not self.remote.version:
            self.remote.get()
        return Version(self.remote.version) <= Version(self.config['version'])
        
    def has_configuration(self):
        return os.path.exists(self.config_path())

    def read_config(self):
        if self.has_configuration():
            return plistlib.readPlist(self.config_path())
    
    def read_repository(self):
        return self.read_config_key('com.robofontmechanic.repository') or self.read_config_key('repository')
    
    def read_config_key(self, key):
        if hasattr(self.config, key):
            return self.config[key]
    
    def config_path(self):
        return os.path.join(self.path, 'info.plist')
        
    def is_configured(self):
        return self.remote is not None
        
    def initialize_remote(self):
        extension_path = self.read_config_key('extensionPath')
        repository = self.read_repository()
        if repository:
            return GithubRepo(repository, 
                              name=self.name,
                              extension_path=extension_path)

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
        
    def get(self):
        """Return the version and location of remote extension."""
        
        postEvent('repositoryWillRead', repository=self)
        
        try:
            if self.extension_path:
                plist_path = os.path.join(self.extension_path, 'info.plist')
                plist_url = self.plist_url % {'repo': self.repo, 'plist_path': plist_path}
                response = requests.get(plist_url)
                response.raise_for_status()
                plist = plistlib.readPlistFromString(response.content)
                self.zip = self.zip_url % {'repo': self.repo}
                self.version = plist['version']
            elif self._get_tags():
                self.tags.sort(key=lambda s: list(Version(s["name"])), reverse=True)
                self.zip = self.tags[0]['zipball_url']
                self.version = self.tags[0]['name']
            else:
                self.zip = self.zip_url % {'repo': self.repo}
        except requests.exceptions.HTTPError:
            print "Couldn't get information about %s from %s" % (self.name, self.repo)
            self.version = '0.0.0'
        
        postEvent('repositoryDidRead', repository=self)
        
    def setup_download(self):
        """Clear extension tmp dir, open download stream and local file."""
        if not hasattr(self,'data'):
            self.get()
        self.tmp_path = os.path.join("/", "tmp", "Mechanic", self.repo)
        self._flush_tmp_path()
        filepath = os.path.join(self.tmp_path, "%s.zip" % os.path.basename(self.zip))
        self.file = open(filepath, "wb")
        self.stream = requests.get(self.zip, stream=True)
        self.stream_content = self.stream.iter_content(chunk_size=8192)
        self.content_length = self.stream.headers['content-length']
    
    def extract_file(self):
        """Extract downloaded zip file and return extension path."""
        zip_file = ZipFile(self.file.name)
        zip_file.extractall(self.tmp_path)
        os.remove(self.file.name)
        
        folder = os.path.join(self.tmp_path, os.listdir(self.tmp_path)[0])
        
        postEvent('repositoryWillExtractDownload', repository=self)
        
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

        postEvent('repositoryDidExtractDownload', repository=self)
        
        return path
    
    def download(self):
        """Download remote version of extension."""

        postEvent('repositoryWillDownload', repository=self)

        self.setup_download()

        try:
            for content in self.stream_content:
                self.file.write(content)
                postEvent('repositoryDidDownloadChunk', 
                          repository=self, 
                          size=self.content_length,
                          downloaded=self.file.tell())
            postEvent('repositoryDidDownload', repository=self)
            return self.extract_file()
        except:
            # ToDo: Make this report different errors
            postEvent('repositoryFailedDownload', repository=self)
            print "Mechanic: Couldn't download %s" % self.name
        finally:
            self.stream.close()
            self.file.close()

    def _get_tags(self):
        response = requests.get(self.tags_url % {'repo': self.repo})
        response.raise_for_status()
        self.tags = response.json()
        return self.tags

    def _flush_tmp_path(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
        mkdir_p(self.tmp_path)

class Registry(object):    
    registry_url = "http://www.robofontmechanic.com/api/v1/registry.json"

    def __init__(self, url=None):
        if url is not None:
            self.registry_url = url
    
    def all(self):
        response = requests.get(self.registry_url)
        response.raise_for_status()
        return response.json()
        
    def add(self, data):
        response = requests.post(self.registry_url, data=data)
        return response
        
class Updates(object):
    
    def __init__(self):
        self.unreachable = False
        
    def all(self, force=False, skip_patch_updates=False):
        if force or self.updatedAt() < time.time() - (60 * 60):
            updates = self._fetchUpdates()
        else:
            updates = self._getCached()
            
        if skip_patch_updates:
            updates = filter(self._filterPatchUpdates, updates)
        
        return updates
    
    def updatedAt(self):
        return Storage.get('cached_at')
        
    def _fetchUpdates(self):
        updates = []
        ignore = Storage.get('ignore')
        for name in ExtensionBundle.allExtensions():
            extension = Extension(name=name)
            if (not extension.bundle.name in ignore and
                    extension.is_configured()):
                try:
                    if not extension.is_current_version():
                        updates.append(extension)
                except:
                    self.unreachable = True
        self._setCached(updates)
        return updates
    
    def _getCached(self):
        cache = Storage.get('cache')
        extensions = []
        for cached in cache.iteritems():
            extension = Extension(name=cached[0])
            if extension.is_configured():
                extension.remote.version = cached[1]
                extensions.append(extension)
        return extensions
        
    def _setCached(self, extensions):
        Storage.set('cached_at', time.time())
        cache = {}
        for extension in extensions:
            cache[extension.bundle.name] = extension.remote.version
        Storage.set('cache', cache)

    def _filterPatchUpdates(self, update):
        local = Version(update.config.version)
        remote = Version(update.remote.version)
        return remote.major > local.major or remote.minor > remote.minor

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
