from AppKit import *
from vanilla import VanillaBaseObject, Sheet, TextBox, ImageView, \
    Button, Group

from mechanic.ui.font import Font


class BaseTab(VanillaBaseObject):
    ns_view_class = NSView
    disabled_text = "Couldn't connect to the Internet..."
    tab_size = (500, 300)

    def __init__(self, dimensions, parent=None):
        self._setupView(self.ns_view_class, dimensions)
        self.parent = parent
        self.content = Group((20, 20, -20, -20))
        self.overlay = DisabledOverlay(self.disabled_text)
        self.setup()

    def setup(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def disable(self):
        self.overlay.show(True)
        print self._getContentView()

    def enable(self):
        self.overlay.show(False)

    def startProgress(self, *args, **kwargs):
        return self.parent.startProgress(*args, **kwargs)

    def closeNotificationSheet(self, sender):
        self.w.notification.close()

    def showNotificationSheet(self, text, size=(300, 80)):
        self.w.notification = Sheet(size, self.parent.w)
        self.w.notification.text = TextBox((15, 15, -50, -15), text)
        self.w.notification.closeButton = Button((-115, -37, 100, 22), 'Close', callback=self.closeNotificationSheet)
        self.w.notification.setDefaultButton(self.parent.w.notification.closeButton)
        self.w.notification.open()

    def showConnectionErrorSheet(self):
        self.showNotificationSheet(self.disabledText)

    def set_default_button(self, button):
        self.w.setDefaultButton(button)

    @property
    def w(self):
        return self.parent.w


class DisabledOverlay(Group):

    def __init__(self, text):
        super(DisabledOverlay, self).__init__((0, 0, -0, -0))
        self.background = Background((0, 0, -0, -0))
        self.disabledText = CenteredText((0, 120, -0, 17), text)
        self.show(False)


class Background(ImageView):

    def __init__(self, dimensions):
        super(Background, self).__init__(dimensions, scale="fit")

        colorTile = NSImage.alloc().initWithSize_((10, 10))
        colorTile.lockFocus()
        color = NSColor.colorWithCalibratedWhite_alpha_(0, 0.65)
        color.set()
        NSRectFillUsingOperation(((0, 0), (10, 10)), NSCompositeSourceOver)
        colorTile.unlockFocus()

        self.setImage(imageObject=colorTile)


class CenteredText(TextBox):

    nsTextFieldClass = NSTextField

    def __init__(self, dimensions, text):
        super(CenteredText, self).__init__(dimensions,
                                           text,
                                           alignment="center")
        self._nsObject.setTextColor_(NSColor.whiteColor())
