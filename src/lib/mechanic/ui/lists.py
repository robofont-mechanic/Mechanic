from AppKit import *
from vanilla import List, CheckBoxListCell, Group
from mojo.extensions import ExtensionBundle

from mechanic.update import Updates
from mechanic.storage import Storage


class ExtensionList(List):

    def _wrapItem(self, extension):
        check = extension.bundle.name not in Storage.get('ignore')
        item = {'name': extension.bundle.name,
                'local_version': extension.config['version'],
                'remote_version': extension.remote.version,
                'install': True,
                'check_for_updates': check,
                'self': extension}

        return super(ExtensionList, self)._wrapItem(item)


class UpdatesList(ExtensionList):
    """Return an ExtensionList for updates window."""

    __columns = [{"title": "Install", "key": "install", "width": 40, "editable": True, "cell": CheckBoxListCell()},
                 {"title": "Extension", "key": "name", "width": 300, "editable": False},
                 {"title": "Version", "key": "remote_version", "width": 60, "editable": False}]

    def __init__(self, posSize, **kwargs):
        kwargs['columnDescriptions'] = self.__columns
        super(UpdatesList, self).__init__(posSize, [], **kwargs)

    def refresh(self, force=False):
        updater = Updates()
        updates = updater.all(force)
        if not updater.unreachable:
            self.set(updates)

    @property
    def selected_extensions(self):
        return [e['self'] for e in self.selected]

    @property
    def selected(self):
        return [row for row in self.get() if row['install']]


class SettingsList(ExtensionList):
    """Return an ExtensionList for settings window."""

    __columns = [{"title": "Check", "key": "check_for_updates", "width": 40, "editable": True, "cell": CheckBoxListCell()},
                 {"title": "Extension", "key": "name", "width": 300, "editable": False},
                 {"title": "Version", "key": "local_version", "editable": False}]

    def __init__(self, *args, **kwargs):
        kwargs['columnDescriptions'] = self.__columns
        super(SettingsList, self).__init__(*args, **kwargs)


class InstallationList(List):
    """Return an ExtensionList for installation window."""

    def __init__(self, posSize, **kwargs):
        columns = [{"title": "Installed",
                    "key": "installed",
                    "width": 25,
                    "editable": False,
                    "cell": InstalledStatusCell.alloc().init()},
                   {"title": "Extension",
                    "key": "extension",
                    "width": 200,
                    "editable": False,
                    "formatter": ExtensionDescriptionFormatter.alloc().init()}]

        super(InstallationList, self).__init__(posSize,
                                               [],
                                               rowHeight=39.0,
                                               columnDescriptions=columns,
                                               showColumnTitles=False,
                                               allowsMultipleSelection=True,
                                               **kwargs)

    def _wrapItem(self, extension):
        name = extension[u'filename'].split("/")[-1]
        item = {'installed': ExtensionBundle(name=name).bundleExists(),
                'extension': extension}
        return super(InstallationList, self)._wrapItem(item)

    def _unwrapListItems(self, items=None):
        if items is None:
            items = super(InstallationList, self).get()
        extensions = [d["extension"] for d in items]
        return extensions

    def set(self, items):
        items = sorted(items, key=lambda e: e['name'].lower())
        super(InstallationList, self).set(items)

    def get(self):
        return self._unwrapListItems()

    def refresh(self):
        self.set(self.get())

    @property
    def selected(self):
        list_ = self.get()
        selections = self.getSelection()
        return [list_[s] for s in selections]


class InstalledStatusCell(NSActionCell):

    def drawWithFrame_inView_(self, frame, view):
        value = self.objectValue()
        if value:
            image = self.drawInstalledIndicator()
            size = image.size()
            x = frame.origin.x + (frame.size.width - size.width) / 2 + 2
            y = frame.origin.y + (frame.size.height - size.height) / 2 - 1
            image.drawAtPoint_fromRect_operation_fraction_((x, y), ((0, 0), (9, 9)), NSCompositeSourceOver, 1.0)

    def drawInstalledIndicator(self):
        image = NSImage.imageNamed_('installedIndicator')
        if image is None:
            width = 9
            height = 9
            image = NSImage.alloc().initWithSize_((width, height))
            image.lockFocus()

            path = NSBezierPath.bezierPathWithOvalInRect_(((0, 0), (9, 9)))
            path.addClip()

            color1 = NSColor.colorWithCalibratedWhite_alpha_(0.0, 0.4)
            color2 = NSColor.colorWithCalibratedWhite_alpha_(0.0, 0.1)

            color1.set()
            path.fill()

            color2.set()
            path.setLineWidth_(2)
            path.stroke()

            image.unlockFocus()
            image.setName_('installedIndicator')
            image = NSImage.imageNamed_('installedIndicator')
        return image


class ExtensionDescriptionFormatter(NSFormatter):

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
