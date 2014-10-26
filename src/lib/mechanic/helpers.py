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


class Storage(object):
    """Convenience class for storing extension settings."""

    defaultKey = "com.jackjennings.mechanic"

    @classmethod
    def generate_key(cls, key):
        return "%s.%s" % (cls.defaultKey, key)

    @classmethod
    def get(cls, key):
        default = cls.generate_key(key)
        return getExtensionDefault(default, fallback=None)

    @classmethod
    def set(cls, key, value):
        default = cls.generate_key(key)
        setExtensionDefault(default, value)
        return value

    @classmethod
    def delete(cls, key):
        default = cls.generate_key(key)
        value = cls.get(key)
        setExtensionDefault(default, None)
        return value

    @classmethod
    def set_defaults(cls, **defaults):
        for key, default in defaults.iteritems():
            value = cls.get(key)
            if value is None:
                print 'Setting default value for %s to %s' % (key, default)
                cls.set(key, default)
