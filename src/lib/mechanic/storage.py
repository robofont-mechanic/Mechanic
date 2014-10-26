from mojo.extensions import getExtensionDefault, setExtensionDefault


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
