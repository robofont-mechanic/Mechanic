from AppKit import *
from vanilla import VanillaBaseObject, Sheet, TextBox, ImageView, \
    Button, Group

from mechanic.ui.font import Font


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
        self.w.notification.close()

    def showNotificationSheet(self, text, size=(300, 80)):
        self.w.notification = Sheet(size, self.parent.w)
        self.w.notification.text = TextBox((15, 15, -50, -15), text)
        self.w.notification.closeButton = Button((-115,-37,100,22), 'Close', callback=self.closeNotificationSheet)
        self.w.notification.setDefaultButton(self.parent.w.notification.closeButton)
        self.w.notification.open()

    def showConnectionErrorSheet(self):
        self.showNotificationSheet(self.disabledText)

    def set_default_button(self, button):
        self.w.setDefaultButton(self.update_button)

    @property
    def w(self):
        return self.parent.w
