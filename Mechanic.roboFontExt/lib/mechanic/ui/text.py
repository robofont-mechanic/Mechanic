from AppKit import NSFontAttributeName, NSFont, NSMutableAttributedString, \
                   NSAttributedString


class Text(object):
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
