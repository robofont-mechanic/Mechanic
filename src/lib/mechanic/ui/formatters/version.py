from AppKit import NSFormatter, NSNull


class VersionFormatter(NSFormatter):

    def stringForObjectValue_(self, obj):
        if obj is None or isinstance(obj, NSNull):
            return ''
        return str(obj)
