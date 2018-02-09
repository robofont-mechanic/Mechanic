import re
import semversion

from mechanic import logger


_re = re.compile(r'^'
                 r'(\d+)\.(\d+)'  # minor, major
                 r'$')


_error = """Version number `%s` is not in a format Mechanic understands.
    Version numbers should conform to the spec described on http://semver.org
    with the exception that it is also possible to use only minor and major
    version numbers in accordance with the RoboFont extension spec. You may
    use pre-release version numbers in the format 1.0.0-alpha, 0.2.1-beta, etc."""


class Version(semversion.Version):
    """
    A slightly less strict version of Version than comes with the version.py
    lib. Accepts versions in the format x.y rather than x.y.z.
    """

    def __init__(self, version):
        version = str(version)
        if _re.match(version):
            version += '.0'

        try:
            super(Version, self).__init__(version)
        except semversion.VersionError:
            logger.warn(_error, version)
            super(Version, self).__init__('0.0.0')
