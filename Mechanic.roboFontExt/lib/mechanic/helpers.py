from AppKit import *
from mojo.extensions import getExtensionDefault, setExtensionDefault


class Font(object):
    """Convenience class for returning NSAttributedStrings."""
    @staticmethod
    def regular(size):
        return {NSFontAttributeName: NSFont.systemFontOfSize_(size)}

    @staticmethod
    def bold(size):
        return {NSFontAttributeName: NSFont.boldSystemFontOfSize_(size)}

    @classmethod
    def string(self, text="", size=13, style="regular", mutable=False):
        if mutable:
            s = NSMutableAttributedString
        else:
            s = NSAttributedString
        weight = getattr(self, style)(size)
        return s.alloc().initWithString_attributes_(text, weight)


class Version(object):
    """Convenience class for comparing version strings."""
    major = 0
    minor = 0
    patch = 0

    def __init__(self, v):
        self.major = 0
        self.minor = 0
        self.patch = 0

        try:
            version = map(int, str(v).split('.'))
            self.major = version[0]
            self.minor = version[1]
            self.patch = version[2]
        except:
            pass

    def __str__(self):
        return "%s.%s.%s" % (self.major, self.minor, self.patch)

    def __iter__(self):
        return iter((self.major, self.minor, self.patch))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return list(self) > list(other)

    def __lt__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)


class Storage(object):
    """Convenience class for storing extension settings."""
    defaults = {"ignore": {},
                "check_on_startup": True,
                "cache": {},
                "cached_at": 0.0,
                "ignore_patch_updates": False}
    defaultKey = "com.jackjennings.mechanic"

    @classmethod
    def genKey(cls, key):
        return "%s.%s" % (cls.defaultKey, key)

    @classmethod
    def get(cls, key):
        default = cls.genKey(key)
        return getExtensionDefault(default, fallback=None)

    @classmethod
    def set(cls, key, value):
        default = cls.genKey(key)
        setExtensionDefault(default, value)
        return value

    @classmethod
    def delete(cls, key):
        default = cls.genKey(key)
        value = cls.get(key)
        setExtensionDefault(default, None)
        return value

    @classmethod
    def setDefaults(cls):
        for key, default in cls.defaults.iteritems():
            value = cls.get(key)
            if value is None:
                print 'Setting default value for %s to %s' % (key, default)
                cls.set(key, default)
