from AppKit import *


class DescriptionFormatter(NSFormatter):

    def stringForObjectValue_(self, obj):
        if obj is None or isinstance(obj, NSNull):
            return ''
        return obj

    def attributedStringForObjectValue_withDefaultAttributes_(self, obj, attrs):
        attrs = dict(attrs)

        paragraph = NSMutableParagraphStyle.alloc().init()
        paragraph.setMinimumLineHeight_(20.0)
        attrs[NSParagraphStyleAttributeName] = paragraph

        string = NSMutableAttributedString.alloc().initWithString_attributes_('', attrs)

        name = NSAttributedString.alloc().initWithString_attributes_(obj['name'] or '', attrs)
        string.appendAttributedString_(name)

        attrs[NSForegroundColorAttributeName] = NSColor.colorWithCalibratedWhite_alpha_(0.6, 1)

        space = NSAttributedString.alloc().initWithString_attributes_(u'\u2003', attrs)
        string.appendAttributedString_(space)

        author = NSAttributedString.alloc().initWithString_attributes_(obj['author'] or '', attrs)
        string.appendAttributedString_(author)

        paragraph = NSMutableParagraphStyle.alloc().init()
        paragraph.setLineBreakMode_(NSLineBreakByTruncatingTail)
        paragraph.setMaximumLineHeight_(14.0)

        attrs[NSParagraphStyleAttributeName] = paragraph
        attrs[NSFontAttributeName] = NSFont.systemFontOfSize_(10.0)

        cr = NSAttributedString.alloc().initWithString_attributes_('\n', attrs)
        string.appendAttributedString_(cr)

        description = NSAttributedString.alloc().initWithString_attributes_(obj['description'] or u'\u2014', attrs)
        string.appendAttributedString_(description)

        return string

    def objectValueForString_(self, string):
        return string
