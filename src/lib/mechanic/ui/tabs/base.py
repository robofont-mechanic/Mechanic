from AppKit import *
from vanilla import VanillaBaseObject, Sheet, TextBox, ImageView, \
    Button, Group

from mechanic.font import Font


class BaseTab(VanillaBaseObject):
    nsViewClass = NSView
    disabledText = "Couldn't connect to the Internet..."
    tabSize = (500, 300)

    def __init__(self, posSize, parent=None):
        self._setupView(self.nsViewClass, posSize)
        self.parent = parent
        self.setup()

    def setup(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def setWindowSize(self):
        self.parent.w.resize(self.tabSize[0], self.tabSize[1], False)

    def disable(self):
        if not hasattr(self, 'disabledOverlay'):
            colorTile = NSImage.alloc().initWithSize_((10, 10))
            colorTile.lockFocus()
            color = NSColor.colorWithCalibratedWhite_alpha_(0, 0.65)
            color.set()
            NSRectFillUsingOperation(((0, 0), (10, 10)), NSCompositeSourceOver)
            colorTile.unlockFocus()

            self.disabledOverlay = Group((0,0,-0,-0))
            self.disabledOverlay.background = ImageView((0, 0, 0, 0), scale="fit")
            self.disabledOverlay.background.setImage(imageObject=colorTile)

            disabledText = Font.string(self.disabledText)
            self.disabledOverlay.disabledText = TextBox((0,120,-0,-0), self.disabledText, alignment="center")
            self.disabledOverlay.disabledText._nsObject.setTextColor_(NSColor.whiteColor())

    def enable(self):
        if hasattr(self, 'disabledOverlay'):
            self.disabledOverlay._nsObject.removeFromSuperview()

    def startProgress(self, *args, **kwargs):
        return self.parent.startProgress(*args, **kwargs)

    def closeNotificationSheet(self, sender):
        self.parent.w.notification.close()

    def showNotificationSheet(self, text, size=(300, 80)):
        self.parent.w.notification = Sheet(size, self.parent.w)
        self.parent.w.notification.text = TextBox((15, 15, -50, -15), text)
        self.parent.w.notification.closeButton = Button((-115,-37,100,22), 'Close', callback=self.closeNotificationSheet)
        self.parent.w.notification.setDefaultButton(self.parent.w.notification.closeButton)
        self.parent.w.notification.open()

    def showConnectionErrorSheet(self):
        self.showNotificationSheet(self.disabledText)
