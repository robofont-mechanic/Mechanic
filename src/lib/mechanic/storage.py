from mojo.extensions import getExtensionDefault, setExtensionDefault

from mechanic import env


class Storage(object):
    """Convenience class for storing extension settings."""

    namespace = "com.jackjennings.mechanic"

    @classmethod
    def generate_key(cls, base):
        return '.'.join((cls.namespace, env.environment, base))

    @classmethod
    def get(cls, base):
        key = cls.generate_key(base)
        return getExtensionDefault(key, fallback=None)

    @classmethod
    def set(cls, base, value):
        key = cls.generate_key(base)
        setExtensionDefault(key, value)
        return value

    @classmethod
    def delete(cls, base):
        key = cls.generate_key(base)
        value = cls.get(base)
        setExtensionDefault(key, None)
        return value

    @classmethod
    def set_defaults(cls, **defaults):
        for key, default in defaults.iteritems():
            value = cls.get(key)
            if value is None:
                print 'Setting default value for %s to %s' % (key, default)
                cls.set(key, default)
