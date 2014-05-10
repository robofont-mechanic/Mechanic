from AppKit import *
from vanilla import List, CheckBoxListCell, Group
from mojo.extensions import ExtensionBundle, getExtensionDefault, setExtensionDefault

class ExtensionList(List):
    
    def _wrapItem(self, extension):
        item = {
                'name': extension.bundle.name,
                'local_version': extension.config['version'],
                'remote_version': extension.remote.version,
                'install': True,
                'check_for_updates': extension.bundle.name not in Storage.get('ignore'),
                'self': extension
               }
        return super(ExtensionList, self)._wrapItem(item)

def UpdatesList(posSize, extensions, **kwargs):
    """Return an ExtensionList for updateable extensions."""
    columns = [
               {"title": "Install", "key": "install", "width": 40, "editable": True, "cell": CheckBoxListCell()}, 
               {"title": "Extension", "key": "name", "width": 300, "editable": False}, 
               {"title": "Version", "key": "remote_version", "width": 60, "editable": False}
              ]
    
    return ExtensionList(posSize, extensions, columnDescriptions=columns, **kwargs)

def SettingsList(posSize, extensions, **kwargs):
    """Return an ExtensionList for settings window."""
    columns = [
               {"title": "Check", "key": "check_for_updates", "width": 40, "editable": True, "cell": CheckBoxListCell()},
               {"title": "Extension", "key": "name", "width": 300, "editable": False},
               {"title": "Version", "key": "local_version", "editable": False}
              ]
    
    return ExtensionList(posSize, extensions, columnDescriptions=columns, **kwargs)

class InstallationList(List):
    """Return an ExtensionList for installation window."""
    
    def __init__(self, posSize, registry, **kwargs):
        columns = [
                   {
                       "title": "Installed", 
                       "key": "installed", 
                       "width": 25, 
                       "editable": False, 
                       "cell": InstalledStatusCell.alloc().init()
                   }, {
                       "title": "Extension", 
                       "key": "extension", 
                       "width": 200, 
                       "editable": False, 
                       "formatter": ExtensionDescriptionFormatter.alloc().init()
                   }
                  ]
        extension_cells = sorted(registry, key=lambda k: k[u'name'].lower())
        return super(InstallationList, self).__init__(posSize, 
                                                      extension_cells, 
                                                      rowHeight=39.0, 
                                                      columnDescriptions=columns, 
                                                      showColumnTitles=False, 
                                                      **kwargs)
    
    def _wrapItem(self, extension):
        item = {
                'installed': ExtensionBundle(name = extension[u'filename'].split("/")[-1]).bundleExists(),
                'extension': extension
               }
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

class Font(object):
    """Convenience class for returning NSAttributedStrings."""
    @staticmethod
    def regular(size): return {NSFontAttributeName:NSFont.systemFontOfSize_(size)}
    
    @staticmethod
    def bold(size): return {NSFontAttributeName:NSFont.boldSystemFontOfSize_(size)}

    @classmethod
    def string(self,text="",size=13,style="regular",mutable=False):
        if mutable == True:
            str = NSMutableAttributedString
        else:
            str = NSAttributedString
        return str.alloc().initWithString_attributes_(text, getattr(self,style)(size))

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
