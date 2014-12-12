import re
import semversion


_re = re.compile('^'
                 '(\d+)\.(\d+)'  # minor, major
                 '$')


class Version(semversion.Version):
    """
    A slightly less strict version of Version than comes with the version.py
    lib. Accepts versions in the format x.y rather than x.y.z.
    """

    def __init__(self, version):
        version = str(version)
        if _re.match(version):
            version += '.0'
        super(Version, self).__init__(version)
